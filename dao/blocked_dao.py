from database.connection import get_connection
from datetime import timedelta, datetime, date



def formatar_timedelta(td):
    if td is None:
        return None
    total_segundos = int(td.total_seconds())
    horas = total_segundos // 3600
    minutos = (total_segundos % 3600) // 60
    segundos = total_segundos % 60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


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
    def bloqueios_do_dia(profissional_id, data=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Pega apenas os horários bloqueados
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

        # Converte para JSON-friendly
        bloqueios = [
            {
                'id': r['id'],
                'data': r['data'].isoformat() if isinstance(r['data'], (date, datetime)) else r['data'],
                'hora_inicio': formatar_timedelta(r['hora_inicio']),
                'hora_fim': formatar_timedelta(r['hora_fim']),
                'motivo': r['motivo']
            }
            for r in registros
        ]

        return bloqueios


    @staticmethod
    def dias_bloqueados(profissional_id, data=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT id, data, motivo
            FROM dias_bloqueados
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

        bloqueios = [
            {
                'id': r['id'],
                'data': r['data'].isoformat() if isinstance(r['data'], (date, datetime)) else r['data'],
                'motivo': r['motivo']
            }
            for r in registros
        ]

        return bloqueios
    

    @staticmethod
    def listar_todos_bloqueios(profissional_id, data=None):
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

        for item in dados:
            if isinstance(item["hora_inicio"], timedelta):
                total_seconds = int(item["hora_inicio"].total_seconds())
                horas = total_seconds // 3600
                minutos = (total_seconds % 3600) // 60
                item["hora_inicio"] = f"{horas:02d}:{minutos:02d}"

            if isinstance(item["hora_fim"], timedelta):
                total_seconds = int(item["hora_fim"].total_seconds())
                horas = total_seconds // 3600
                minutos = (total_seconds % 3600) // 60
                item["hora_fim"] = f"{horas:02d}:{minutos:02d}"

        cursor.close()
        conn.close()

        return dados


    @staticmethod
    def apagar_bloqueios_dia(bloqueio_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM dias_bloqueados WHERE id = %s",
            (bloqueio_id,)
        )

        conn.commit()
        afetados = cursor.rowcount

        cursor.close()
        conn.close()

        return afetados > 0
    
    @staticmethod
    def apagar_bloqueios_horario(bloqueio_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM horarios_bloqueados WHERE id = %s",
            (bloqueio_id,)
        )

        conn.commit()
        afetados = cursor.rowcount

        cursor.close()
        conn.close()

        return afetados > 0