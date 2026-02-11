from database.connection import get_connection
from datetime import timedelta, datetime


class BloqueioDAO:

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
    def bloquear_periodo(profissional_id, data_inicio, data_fim, motivo=None):


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


    @staticmethod
    def criar(profissional_id, data, hora_inicio=None, hora_fim=None):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO bloqueios
            (profissional_id, data, hora_inicio, hora_fim)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (profissional_id, data, hora_inicio, hora_fim)
        )

        conn.commit()
        cursor.close()
        conn.close()


    @staticmethod
    def bloqueios_do_dia(profissional_id, data):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                data,
                hora_inicio,
                hora_fim
            FROM bloqueios
            WHERE profissional_id = %s
              AND data = %s
        """, (profissional_id, data))

        bloqueios = cursor.fetchall()

        cursor.close()
        conn.close()

        return bloqueios
    

    @staticmethod
    def listar_bloqueios(profissional_id, data=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT *
            FROM bloqueios
            WHERE profissional_id = %s
        """

        params = [profissional_id]

        if data:
            query += " AND data = %s"
            params.append(data)

        cursor.execute(query, params)
        dados = cursor.fetchall()

        cursor.close()
        conn.close()

        return dados

    @staticmethod
    def apagar_bloqueios(bloqueio_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM bloqueios WHERE id = %s",
            (bloqueio_id,)
        )

        conn.commit()
        afetados = cursor.rowcount

        cursor.close()
        conn.close()

        return afetados > 0