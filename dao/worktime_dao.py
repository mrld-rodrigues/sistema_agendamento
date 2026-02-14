from database.connection import get_connection
from datetime import time, timedelta


class HorariosTrabalhoDAO:    

    @staticmethod
    def criar(profissional_id, dia_semana, hora_inicio, hora_fim):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO horarios_trabalho
            (profissional_id, dia_semana, hora_inicio, hora_fim)
            VALUES (%s, %s, %s, %s)
        """, (profissional_id, dia_semana, hora_inicio, hora_fim))
        conn.commit()
        novo_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return novo_id

    @staticmethod
    def listar_por_profissional(profissional_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, dia_semana, hora_inicio, hora_fim
            FROM horarios_trabalho
            WHERE profissional_id = %s
            ORDER BY dia_semana, hora_inicio
        """, (profissional_id,))
        dados = cursor.fetchall()
        cursor.close()
        conn.close()
        # Converter timedelta para string HH:MM
        for d in dados:
            if isinstance(d['hora_inicio'], timedelta):
                d['hora_inicio'] = str(d['hora_inicio'])[:-3]  # HH:MM:SS -> HH:MM
            if isinstance(d['hora_fim'], timedelta):
                d['hora_fim'] = str(d['hora_fim'])[:-3]
        return dados

    @staticmethod
    def buscar_por_id(id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, profissional_id, dia_semana, hora_inicio, hora_fim
            FROM horarios_trabalho
            WHERE id = %s
        """, (id,))
        dado = cursor.fetchone()
        cursor.close()
        conn.close()
        if dado:
            if isinstance(dado['hora_inicio'], timedelta):
                dado['hora_inicio'] = str(dado['hora_inicio'])[:-3]
            if isinstance(dado['hora_fim'], timedelta):
                dado['hora_fim'] = str(dado['hora_fim'])[:-3]
        return dado

    @staticmethod
    def atualizar(id, dia_semana=None, hora_inicio=None, hora_fim=None):
        conn = get_connection()
        cursor = conn.cursor()
        campos = []
        params = []
        if dia_semana is not None:
            campos.append("dia_semana = %s")
            params.append(dia_semana)
        if hora_inicio is not None:
            campos.append("hora_inicio = %s")
            params.append(hora_inicio)
        if hora_fim is not None:
            campos.append("hora_fim = %s")
            params.append(hora_fim)
        if not campos:
            return False
        params.append(id)
        query = f"UPDATE horarios_trabalho SET {', '.join(campos)} WHERE id = %s"
        cursor.execute(query, params)
        conn.commit()
        afetados = cursor.rowcount
        cursor.close()
        conn.close()
        return afetados > 0

    @staticmethod
    def deletar(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM horarios_trabalho WHERE id = %s", (id,))
        afetados = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return afetados > 0    


    @staticmethod
    def buscar_por_profissional_e_dia(profissional_id, dia_semana):
        """
        Retorna os horários de trabalho de um profissional para um determinado dia da semana.
        Os campos 'hora_inicio' e 'hora_fim' são convertidos para objetos time.
        
        :param profissional_id: ID do profissional
        :param dia_semana: dia da semana (0=segunda, 6=domingo)
        :return: lista de dicionários com 'hora_inicio' e 'hora_fim' como objetos time
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT hora_inicio, hora_fim
            FROM horarios_trabalho
            WHERE profissional_id = %s AND dia_semana = %s
        """, (profissional_id, dia_semana))
        dados = cursor.fetchall()
        cursor.close()
        conn.close()

        resultados = []
        for d in dados:
            # Converte timedelta para time
            def timedelta_to_time(td):
                if isinstance(td, timedelta):
                    total_seconds = int(td.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    seconds = total_seconds % 60
                    return time(hours, minutes, seconds)
                return td  # se já for time, mantém (improvável)

            d['hora_inicio'] = timedelta_to_time(d['hora_inicio'])
            d['hora_fim'] = timedelta_to_time(d['hora_fim'])
            resultados.append(d)
        return resultados