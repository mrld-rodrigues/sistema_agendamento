from database.connection import get_connection


class HorariosTrabalhoDAO:

    @staticmethod
    def buscar_por_profissional_e_dia(profissional_id, dia_semana):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT hora_inicio, hora_fim
            FROM horarios_trabalho
            WHERE profissional_id = %s
              AND dia_semana = %s
        """, (profissional_id, dia_semana))

        dados = cursor.fetchall()

        cursor.close()
        conn.close()

        return dados
