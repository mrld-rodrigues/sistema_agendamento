from database.connection import get_connection
from datetime import time, timedelta, datetime, date

def formatar_timedelta(td):
    """Auxiliar para converter timedelta em string HH:MM:SS (usado nas consultas antigas)"""
    if td is None:
        return None
    total_segundos = int(td.total_seconds())
    horas = total_segundos // 3600
    minutos = (total_segundos % 3600) // 60
    segundos = total_segundos % 60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

class BloqueioDAO:

    # ---------- Bloqueios de dia inteiro ----------
    @staticmethod
    def bloquear_dia(profissional_id, data, motivo=None):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO dias_bloqueados (profissional_id, data, motivo)
            VALUES (%s, %s, %s)
        """, (profissional_id, data, motivo))
        conn.commit()
        cursor.close()
        conn.close()


    @staticmethod
    def dias_bloqueados(profissional_id, data=None):
        """Retorna todos os dias bloqueados de um profissional (opcionalmente filtrando por data)"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, data, motivo FROM dias_bloqueados WHERE profissional_id = %s"
        params = [profissional_id]
        if data:
            query += " AND data = %s"
            params.append(data)
        cursor.execute(query, params)
        registros = cursor.fetchall()
        cursor.close()
        conn.close()
        # Converte date para string ISO (para JSON)
        for r in registros:
            if isinstance(r['data'], (date, datetime)):
                r['data'] = r['data'].isoformat()
        return registros


    # ---------- Bloqueios de horário específico ----------
    @staticmethod
    def bloquear_horario(profissional_id, data, inicio, fim, motivo=None):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO horarios_bloqueados
            (profissional_id, data, hora_inicio, hora_fim, motivo)
            VALUES (%s, %s, %s, %s, %s)
        """, (profissional_id, data, inicio, fim, motivo))
        conn.commit()
        cursor.close()
        conn.close()


    @staticmethod
    def horarios_bloqueados_do_dia(profissional_id, data=None):
        """
        Retorna apenas os bloqueios de horário (tabela horarios_bloqueados).
        Antigo nome 'bloqueios_do_dia' foi renomeado para maior clareza.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT id, data, hora_inicio, hora_fim, motivo
            FROM horarios_bloqueados
            WHERE profissional_id = %s
        """
        params = [profissional_id]
        if data:
            query += " AND data = %s"
            params.append(data)
        cursor.execute(query, params)
        registros = cursor.fetchall()
        cursor.close()
        conn.close()
        # Converte timedelta para string HH:MM e date para string
        bloqueios = []
        for r in registros:
            item = {
                'id': r['id'],
                'data': r['data'].isoformat() if isinstance(r['data'], (date, datetime)) else r['data'],
                'hora_inicio': formatar_timedelta(r['hora_inicio']),
                'hora_fim': formatar_timedelta(r['hora_fim']),
                'motivo': r['motivo']
            }
            bloqueios.append(item)
        return bloqueios


    # ---------- Bloqueios de período (vários dias) ----------
    @staticmethod
    def bloquear_periodo(profissional_id, data_inicio, data_fim, motivo=None):
        """Bloqueia uma sequência de dias (insere em dias_bloqueados para cada dia)"""
        conn = get_connection()
        cursor = conn.cursor()
        inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
        dia_atual = inicio
        while dia_atual <= fim:
            cursor.execute("""
                INSERT IGNORE INTO dias_bloqueados
                (profissional_id, data, motivo)
                VALUES (%s, %s, %s)
            """, (profissional_id, dia_atual, motivo))
            dia_atual += timedelta(days=1)
        conn.commit()
        cursor.close()
        conn.close()


    # ---------- Bloqueios recorrentes (semanais) ----------
    @staticmethod
    def criar_bloqueio_recorrente(profissional_id, dia_semana, hora_inicio, hora_fim,
                                  data_inicio=None, data_fim=None, motivo=None):
        """
        Cria um bloqueio que se repete semanalmente em um dia da semana.
        dia_semana: 0=segunda, 1=terça, ..., 6=domingo (padrão Python).
        data_inicio e data_fim são opcionais para limitar a validade.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bloqueios_recorrentes
            (profissional_id, dia_semana, hora_inicio, hora_fim, data_inicio, data_fim, motivo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (profissional_id, dia_semana, hora_inicio, hora_fim, data_inicio, data_fim, motivo))
        conn.commit()
        novo_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return novo_id


    @staticmethod
    def listar_bloqueios_recorrentes(profissional_id=None, data_referencia=None):
        """
        Lista os bloqueios recorrentes.
        Se data_referencia for fornecida (date ou string YYYY-MM-DD), retorna apenas os
        que estão ativos nessa data (considerando data_inicio, data_fim e dia_semana).
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM bloqueios_recorrentes WHERE 1=1"
        params = []
        if profissional_id:
            query += " AND profissional_id = %s"
            params.append(profissional_id)
        if data_referencia:
            if isinstance(data_referencia, str):
                data_referencia = datetime.strptime(data_referencia, "%Y-%m-%d").date()
            query += """ AND (data_inicio IS NULL OR data_inicio <= %s)
                         AND (data_fim IS NULL OR data_fim >= %s)
                         AND dia_semana = %s """
            params.extend([data_referencia, data_referencia, data_referencia.weekday()])
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        # Converte timedelta para string HH:MM e date para string
        for r in resultados:
            if isinstance(r['hora_inicio'], timedelta):
                r['hora_inicio'] = formatar_timedelta(r['hora_inicio'])
            if isinstance(r['hora_fim'], timedelta):
                r['hora_fim'] = formatar_timedelta(r['hora_fim'])
            if isinstance(r['data_inicio'], (date, datetime)):
                r['data_inicio'] = r['data_inicio'].isoformat() if r['data_inicio'] else None
            if isinstance(r['data_fim'], (date, datetime)):
                r['data_fim'] = r['data_fim'].isoformat() if r['data_fim'] else None
        return resultados


    @staticmethod
    def apagar_bloqueio_recorrente(bloqueio_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bloqueios_recorrentes WHERE id = %s", (bloqueio_id,))
        afetados = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return afetados > 0


    # ---------- Unificação de todos os bloqueios para um dia específico ----------
    @staticmethod
    def listar_todos_bloqueios_do_dia(profissional_id, data):
        """
        Retorna uma lista de dicionários com 'inicio', 'fim' (datetime) e 'tipo'
        para todos os bloqueios que afetam o profissional na data fornecida.
        Inclui: dias inteiros, horários específicos e bloqueios recorrentes ativos.
        Útil para o motor de horários livres.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        bloqueios = []

        # 1. Dias inteiros
        cursor.execute("""
            SELECT data, motivo FROM dias_bloqueados
            WHERE profissional_id = %s AND data = %s
        """, (profissional_id, data))
        dias = cursor.fetchall()
        for d in dias:
            inicio = datetime.combine(d['data'], datetime.min.time())
            fim = datetime.combine(d['data'], datetime.max.time())
            bloqueios.append({
                'inicio': inicio,
                'fim': fim,
                'motivo': d['motivo'],
                'tipo': 'dia'
            })

        # 2. Horários bloqueados
        cursor.execute("""
            SELECT data, hora_inicio, hora_fim, motivo FROM horarios_bloqueados
            WHERE profissional_id = %s AND data = %s
        """, (profissional_id, data))
        horarios = cursor.fetchall()
        for h in horarios:
            inicio = datetime.combine(h['data'], h['hora_inicio'])
            fim = datetime.combine(h['data'], h['hora_fim'])
            bloqueios.append({
                'inicio': inicio,
                'fim': fim,
                'motivo': h['motivo'],
                'tipo': 'horario'
            })

       # 3. Bloqueios recorrentes ativos na data
        dia_semana = data.weekday()  # 0=segunda, 6=domingo
        cursor.execute("""
            SELECT hora_inicio, hora_fim, motivo FROM bloqueios_recorrentes
            WHERE profissional_id = %s
            AND dia_semana = %s
            AND (data_inicio IS NULL OR data_inicio <= %s)
            AND (data_fim IS NULL OR data_fim >= %s)
        """, (profissional_id, dia_semana, data, data))
        recorrentes = cursor.fetchall()

        # Função auxiliar para converter timedelta para time
        def timedelta_to_time(td):
            if isinstance(td, timedelta):
                total_seconds = int(td.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                return time(hours, minutes, seconds)
            return td  # se já for time (improvável)

        for r in recorrentes:
            hora_inicio = timedelta_to_time(r['hora_inicio'])
            hora_fim = timedelta_to_time(r['hora_fim'])
            inicio = datetime.combine(data, hora_inicio)
            fim = datetime.combine(data, hora_fim)
            bloqueios.append({
                'inicio': inicio,
                'fim': fim,
                'motivo': r['motivo'],
                'tipo': 'recorrente'
            })


    # ---------- Listagem geral (para consultas administrativas) ----------
    @staticmethod
    def listar_todos_bloqueios(profissional_id, data=None):
        """
        Retorna a união de dias_bloqueados e horarios_bloqueados (sem os recorrentes).
        Mantido para compatibilidade com rotas existentes.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                id,
                profissional_id,
                data,
                NULL AS hora_inicio,
                NULL AS hora_fim,
                motivo,
                'dia' AS tipo
            FROM dias_bloqueados
            WHERE profissional_id = %s
        """
        params = [profissional_id]

        if data:
            query += " AND data = %s"
            params.append(data)

        query += """
            UNION ALL
            SELECT
                id,
                profissional_id,
                data,
                hora_inicio,
                hora_fim,
                motivo,
                'horario' AS tipo
            FROM horarios_bloqueados
            WHERE profissional_id = %s
        """
        params.append(profissional_id)

        if data:
            query += " AND data = %s"
            params.append(data)

        query += " ORDER BY data, hora_inicio"

        cursor.execute(query, params)
        dados = cursor.fetchall()

        # Formata timedelta para string HH:MM
        for item in dados:
            if isinstance(item["hora_inicio"], timedelta):
                item["hora_inicio"] = formatar_timedelta(item["hora_inicio"])
            if isinstance(item["hora_fim"], timedelta):
                item["hora_fim"] = formatar_timedelta(item["hora_fim"])
            if isinstance(item["data"], (date, datetime)):
                item["data"] = item["data"].isoformat()

        cursor.close()
        conn.close()
        return dados


    # ---------- Deleções ----------
    @staticmethod
    def apagar_bloqueios_dia(bloqueio_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM dias_bloqueados WHERE id = %s", (bloqueio_id,))
        afetados = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return afetados > 0


    @staticmethod
    def apagar_bloqueios_horario(bloqueio_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM horarios_bloqueados WHERE id = %s", (bloqueio_id,))
        afetados = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return afetados > 0
        

    @staticmethod
    def verificar_conflito_bloqueios(profissional_id, inicio_intervalo, fim_intervalo):
        """
        Verifica se há conflito com qualquer tipo de bloqueio (dia, horário, recorrente).
        Retorna True se houver sobreposição.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        data_intervalo = inicio_intervalo.date()

        # 1. Verificar dia inteiro
        cursor.execute("""
            SELECT id FROM dias_bloqueados
            WHERE profissional_id = %s AND data = %s
        """, (profissional_id, data_intervalo))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return True

        # 2. Verificar horários bloqueados específicos
        cursor.execute("""
            SELECT id FROM horarios_bloqueados
            WHERE profissional_id = %s
            AND data = %s
            AND hora_inicio < %s
            AND hora_fim > %s
        """, (profissional_id, data_intervalo, fim_intervalo.time(), inicio_intervalo.time()))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return True

        # 3. Verificar bloqueios recorrentes ativos na data
        dia_semana = data_intervalo.weekday()
        cursor.execute("""
            SELECT id FROM bloqueios_recorrentes
            WHERE profissional_id = %s
            AND dia_semana = %s
            AND (data_inicio IS NULL OR data_inicio <= %s)
            AND (data_fim IS NULL OR data_fim >= %s)
            AND hora_inicio < %s
            AND hora_fim > %s
        """, (
            profissional_id,
            dia_semana,
            data_intervalo, data_intervalo,
            fim_intervalo.time(), inicio_intervalo.time()
        ))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return True

        cursor.close()
        conn.close()
        return False