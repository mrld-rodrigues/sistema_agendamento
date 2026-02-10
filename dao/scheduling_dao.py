from database.connection import get_connection
from datetime import timedelta, datetime


class AgendamentoDAO:

    @staticmethod
    def criar(cliente_id, profissional_id, servico_id, data_hora):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO agendamentos
            (cliente_id, profissional_id, servico_id, data_hora)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (cliente_id, profissional_id, servico_id, data_hora)
        )

        conn.commit()
        agendamento_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return agendamento_id
    

    @staticmethod
    def verificar_conflito(profissional_id, data_hora_inicio, duracao_minutos):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        data_hora_fim = data_hora_inicio + timedelta(minutes=duracao_minutos)

        query = """
            SELECT a.id
            FROM agendamentos a
            JOIN servicos s ON s.id = a.servico_id
            WHERE a.profissional_id = %s
              AND (
                a.data_hora < %s
                AND DATE_ADD(a.data_hora, INTERVAL s.duracao_minutos MINUTE) > %s
              )
        """

        cursor.execute(
            query,
            (profissional_id, data_hora_fim, data_hora_inicio)
        )

        conflito = cursor.fetchone()

        cursor.close()
        conn.close()

        return conflito is not None    
    

    @staticmethod
    def listar_por_profissional_e_data(profissional_id, data):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                a.id,
                a.data_hora,
                c.nome AS cliente,
                s.nome AS servico,
                s.duracao_minutos,
                s.preco
            FROM agendamentos a
            JOIN clientes c ON c.id = a.cliente_id
            JOIN servicos s ON s.id = a.servico_id
            WHERE a.profissional_id = %s
              AND DATE(a.data_hora) = %s
            ORDER BY a.data_hora
        """

        cursor.execute(query, (profissional_id, data))
        resultados = cursor.fetchall()

        cursor.close()
        conn.close()

        return resultados


    @staticmethod
    def listar_semana(profissional_id, data_inicio):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                a.id,
                a.data_hora,
                c.nome AS cliente,
                s.nome AS servico,
                s.duracao_minutos
            FROM agendamentos a
            JOIN clientes c ON c.id = a.cliente_id
            JOIN servicos s ON s.id = a.servico_id
            WHERE a.profissional_id = %s
              AND a.data_hora BETWEEN %s AND DATE_ADD(%s, INTERVAL 7 DAY)
            ORDER BY a.data_hora
        """

        cursor.execute(query, (profissional_id, data_inicio, data_inicio))
        dados = cursor.fetchall()

        cursor.close()
        conn.close()

        return dados
    

    @staticmethod
    def buscar_do_dia(profissional_id, data):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT a.data_hora, s.duracao_minutos
            FROM agendamentos a
            JOIN servicos s ON s.id = a.servico_id
            WHERE a.profissional_id = %s
              AND DATE(a.data_hora) = %s
            ORDER BY a.data_hora
        """, (profissional_id, data))

        dados = cursor.fetchall()

        cursor.close()
        conn.close()

        return dados


    @staticmethod
    def calendario_mensal(profissional_id, ano, mes):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                DATE(a.data_hora) AS dia,
                COUNT(*) AS total_agendamentos
            FROM agendamentos a
            WHERE a.profissional_id = %s
            AND YEAR(a.data_hora) = %s
            AND MONTH(a.data_hora) = %s
            GROUP BY DATE(a.data_hora)
            ORDER BY dia
        """

        cursor.execute(query, (profissional_id, ano, mes))
        dados = cursor.fetchall()

        cursor.close()
        conn.close()

        return dados
    

    @staticmethod
    def calendario_completo(profissional_id, ano, mes):
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                d.dia,
                COALESCE(a.total, 0) AS total_agendamentos,
                CASE
                    WHEN b.data IS NOT NULL THEN 'bloqueado'
                    WHEN a.total IS NOT NULL THEN 'ocupado'
                    ELSE 'livre'
                END AS status
            FROM (
                SELECT DATE(CONCAT(%s,'-',%s,'-01')) + INTERVAL seq DAY AS dia
                FROM (
                    SELECT 0 seq UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION
                    SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION
                    SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11 UNION
                    SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15 UNION
                    SELECT 16 UNION SELECT 17 UNION SELECT 18 UNION SELECT 19 UNION
                    SELECT 20 UNION SELECT 21 UNION SELECT 22 UNION SELECT 23 UNION
                    SELECT 24 UNION SELECT 25 UNION SELECT 26 UNION SELECT 27 UNION
                    SELECT 28 UNION SELECT 29 UNION SELECT 30 UNION SELECT 31
                ) seqs
            ) d
            LEFT JOIN (
                SELECT DATE(data_hora) dia, COUNT(*) total
                FROM agendamentos
                WHERE profissional_id = %s
                GROUP BY DATE(data_hora)
            ) a ON a.dia = d.dia
            LEFT JOIN dias_bloqueados b
              ON b.data = d.dia AND b.profissional_id = %s
            WHERE MONTH(d.dia) = %s
        """

        cursor.execute(
            query,
            (ano, mes, profissional_id, profissional_id, mes)
        )

        dados = cursor.fetchall()

        cursor.close()
        conn.close()

        return dados
  
  
    @staticmethod
    def agendamentos_do_dia(profissional_id, data):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT data_hora, duracao_minutos
            FROM agendamentos
            WHERE profissional_id = %s
            AND DATE(data_hora) = %s
            ORDER BY data_hora
        """, (profissional_id, data))

        dados = cursor.fetchall()

        cursor.close()
        conn.close()

        return dados


    @staticmethod
    def listar(data=None, profissional_id=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                a.id,
                a.data_hora,
                c.nome AS cliente,
                p.nome AS profissional,
                s.nome AS servico,
                s.duracao_minutos
            FROM agendamentos a
            JOIN clientes c ON c.id = a.cliente_id
            JOIN profissionais p ON p.id = a.profissional_id
            JOIN servicos s ON s.id = a.servico_id
            WHERE 1=1
        """

        params = []

        if data:
            query += " AND DATE(a.data_hora) = %s"
            params.append(data)

        if profissional_id:
            query += " AND a.profissional_id = %s"
            params.append(profissional_id)

        query += " ORDER BY a.data_hora"

        cursor.execute(query, params)
        resultados = cursor.fetchall()

        cursor.close()
        conn.close()

        return resultados
