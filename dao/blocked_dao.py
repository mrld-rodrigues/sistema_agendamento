from database.connection import get_connection


class BloqueiosDAO:
    @staticmethod
    def bloqueios_do_dia(profissional_id, data):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT hora_inicio, hora_fim
            FROM horarios_bloqueados
            WHERE profissional_id = %s
            AND data = %s
        """, (profissional_id, data))

        dados = cursor.fetchall()

        cursor.close()
        conn.close()

        return dados
