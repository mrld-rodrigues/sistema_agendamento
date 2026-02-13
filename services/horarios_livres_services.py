from datetime import timedelta
from dao.scheduling_dao import AgendamentoDAO
from dao.blocked_dao import BloqueioDAO


class HorariosLivresService:
    
    @staticmethod
    def verificar_disponibilidade(profissional_id, data_hora_inicio, duracao_minutos, ignorar_agendamento_id=None):
        """
        Retorna True se o horário estiver disponível (sem conflitos de agendamentos ou bloqueios).
        """
        # Verificar agendamentos
        if AgendamentoDAO.verificar_conflito_agendamentos(
            profissional_id,
            data_hora_inicio,
            duracao_minutos,
            ignorar_agendamento_id
        ):
            return False

        # Verificar bloqueios
        data_hora_fim = data_hora_inicio + timedelta(minutes=duracao_minutos)
        if BloqueioDAO.verificar_conflito_bloqueios(
            profissional_id,
            data_hora_inicio,
            data_hora_fim
        ):
            return False

        return True

    @staticmethod
    def calcular_horarios_livres(profissional_id, data, duracao_necessaria=None, servico_id=None):
        """
        Retorna lista de horários de início disponíveis para um profissional em uma data.
        """
        # Implementação será baseada no método antigo, mas usando os novos métodos de bloqueio.
        # Vamos manter a lógica existente e ajustar para usar os novos métodos.
        # Por enquanto, manteremos o código atual da rota /horarios-livres, mas movendo para cá.
        pass