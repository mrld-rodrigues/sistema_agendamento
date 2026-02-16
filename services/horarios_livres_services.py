from datetime import datetime, timedelta, time
from dao.scheduling_dao import AgendamentoDAO
from dao.blocked_dao import BloqueioDAO
from dao.worktime_dao import HorariosTrabalhoDAO
from dao.professional_dao import ProfissionalDAO

class HorariosLivresService:
    
    @staticmethod
    def verificar_disponibilidade(profissional_id, data_hora_inicio, duracao_minutos, ignorar_agendamento_id=None):
        """
        Verifica se um profissional está disponível em um determinado horário.
        Retorna True se disponível, False caso contrário.
        """
        data_hora_fim = data_hora_inicio + timedelta(minutes=duracao_minutos)

        # Obter buffer do profissional
        profissional = ProfissionalDAO.buscar_por_id(profissional_id)
        buffer = profissional.get('intervalo_minutos', 0) if profissional else 0

        # Verificar conflito com agendamentos (incluindo buffer)
        if AgendamentoDAO.verificar_conflito(
            profissional_id,
            data_hora_inicio,
            data_hora_fim,
            ignorar_agendamento_id,
            buffer
        ):
            return False

        # Verificar conflito com bloqueios (usando método otimizado)
        if BloqueioDAO.verificar_conflito_bloqueios(
            profissional_id,
            data_hora_inicio,
            data_hora_fim
        ):
            return False

        return True

    @staticmethod
    def calcular_horarios_livres(profissional_id, data, duracao_necessaria=None):
        """
        Retorna uma lista de tuplas (inicio, fim) representando os intervalos
        de tempo livres para um profissional em uma determinada data.
        
        :param profissional_id: ID do profissional
        :param data: objeto date da data desejada
        :param duracao_necessaria: duração em minutos do serviço (se None, retorna todos os intervalos livres)
        :return: lista de tuplas (datetime_inicio, datetime_fim) com os intervalos livres
        """
        # 1. Obter a jornada de trabalho do profissional para o dia da semana
        dia_semana = data.weekday()  # 0=segunda, 6=domingo
        jornadas = HorariosTrabalhoDAO.buscar_por_profissional_e_dia(profissional_id, dia_semana)
        
        if not jornadas:
            return []  # Não trabalha neste dia

        # 2. Obter todos os eventos ocupados: agendamentos + bloqueios
        # Agendamentos do dia (já com data_hora e duracao)
        agendamentos = AgendamentoDAO.buscar_do_dia(profissional_id, data)
        
        # Bloqueios do dia (inclui dias inteiros, horários e recorrentes)
        bloqueios = BloqueioDAO.listar_todos_bloqueios_do_dia(profissional_id, data)

        # 3. Converter agendamentos para eventos com inicio e fim
        eventos = []
        for a in agendamentos:
            inicio = a['data_hora']
            fim = inicio + timedelta(minutes=a['duracao_minutos'])
            eventos.append({'inicio': inicio, 'fim': fim, 'tipo': 'agendamento'})

        # Adicionar bloqueios (já estão com inicio e fim como datetime)
        for b in bloqueios:
            eventos.append({'inicio': b['inicio'], 'fim': b['fim'], 'tipo': b['tipo']})

        # 4. Ordenar eventos por inicio
        eventos.sort(key=lambda e: e['inicio'])

        # 5. Obter intervalo de buffer do profissional (tempo entre atendimentos)
        profissional = ProfissionalDAO.buscar_por_id(profissional_id)
        intervalo_buffer = profissional.get('intervalo_minutos', 0) if profissional else 0

        # 6. Para cada período de jornada, calcular intervalos livres
        intervalos_livres = []

        for j in jornadas:
            # Converter hora_inicio e hora_fim para objetos time
            if isinstance(j['hora_inicio'], str):
                hora_inicio = datetime.strptime(j['hora_inicio'], '%H:%M').time()
            else:
                hora_inicio = j['hora_inicio']
            
            if isinstance(j['hora_fim'], str):
                hora_fim = datetime.strptime(j['hora_fim'], '%H:%M').time()
            else:
                hora_fim = j['hora_fim']

            inicio_jornada = datetime.combine(data, hora_inicio)
            fim_jornada = datetime.combine(data, hora_fim)

            # Se a jornada passa da meia-noite (ex.: 22:00 às 02:00), ajusta o fim para o dia seguinte
            if fim_jornada <= inicio_jornada:
                fim_jornada += timedelta(days=1)

            # Recortar eventos que intersectam este período
            fatias = [(inicio_jornada, fim_jornada)]
            
            for evento in eventos:
                # Se evento está completamente fora, ignorar
                if evento['fim'] <= inicio_jornada or evento['inicio'] >= fim_jornada:
                    continue
                
                novas_fatias = []
                for fatia_inicio, fatia_fim in fatias:
                    # Parte antes do evento
                    if fatia_inicio < evento['inicio']:
                        novas_fatias.append((fatia_inicio, min(fatia_fim, evento['inicio'])))
                    # Parte depois do evento
                    if fatia_fim > evento['fim']:
                        novas_fatias.append((max(fatia_inicio, evento['fim'] + timedelta(minutes=intervalo_buffer)), fatia_fim))
                fatias = novas_fatias

            # Adicionar as fatias resultantes à lista de intervalos livres
            intervalos_livres.extend(fatias)

        # 7. Se duracao_necessaria for fornecida, filtrar apenas intervalos que comportam a duração
        if duracao_necessaria:
            intervalos_filtrados = []
            for inicio, fim in intervalos_livres:
                if (fim - inicio).total_seconds() / 60 >= duracao_necessaria:
                    intervalos_filtrados.append((inicio, fim))
            return intervalos_filtrados

        return intervalos_livres