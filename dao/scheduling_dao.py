from database.connection import get_connection
from datetime import timedelta


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
    def buscar_por_id(agendamento_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT a.*, s.duracao_minutos, s.nome as servico_nome, c.nome as cliente_nome, p.nome as profissional_nome
            FROM agendamentos a
            JOIN servicos s ON s.id = a.servico_id
            JOIN clientes c ON c.id = a.cliente_id
            JOIN profissionais p ON p.id = a.profissional_id
            WHERE a.id = %s
        """
        cursor.execute(query, (agendamento_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result


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
            SELECT a.id, a.data_hora, s.duracao_minutos
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


    @staticmethod
    def remarcar(agendamento_id, nova_data_hora):
        """
        Atualiza a data/hora de um agendamento. Não faz validações.
        Retorna True se atualizou, False caso contrário.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE agendamentos SET data_hora = %s WHERE id = %s",
            (nova_data_hora, agendamento_id)
        )
        afetados = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return afetados > 0
    

    @staticmethod
    def deletar(agendamento_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM agendamentos WHERE id = %s",
            (agendamento_id,)
        )

        afetados = cursor.rowcount

        conn.commit()
        cursor.close()
        conn.close()

        return afetados > 0
    

    @staticmethod
    def verificar_conflito(profissional_id, inicio_intervalo, fim_intervalo, ignorar_agendamento_id=None, buffer_minutos=0):
        """
        Verifica se há conflito com outros agendamentos considerando buffer.
        Retorna True se houver conflito, False caso contrário.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT COUNT(*) as total
            FROM agendamentos a
            JOIN servicos s ON a.servico_id = s.id
            WHERE a.profissional_id = %s
            AND a.data_hora < %s
            AND DATE_ADD(a.data_hora, INTERVAL s.duracao_minutos + %s MINUTE) > %s
        """
        params = [profissional_id, fim_intervalo, buffer_minutos, inicio_intervalo]
        
        if ignorar_agendamento_id:
            query += " AND a.id != %s"
            params.append(ignorar_agendamento_id)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return result['total'] > 0
        

    @staticmethod
    def verificar_conflito_com_buffer(profissional_id, inicio_intervalo, fim_intervalo, buffer_minutos, ignorar_agendamento_id=None):
        """
        Verifica se há conflito com outros agendamentos considerando o buffer após cada atendimento.
        Retorna True se houver conflito.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT a.id
            FROM agendamentos a
            JOIN servicos s ON a.servico_id = s.id
            WHERE a.profissional_id = %s
            AND (
                DATE_ADD(a.data_hora, INTERVAL s.duracao_minutos + %s MINUTE) > %s
                OR
                a.data_hora < DATE_ADD(%s, INTERVAL %s + %s MINUTE)
            )
        """
        params = [profissional_id, buffer_minutos, inicio_intervalo, fim_intervalo, (fim_intervalo - inicio_intervalo).seconds // 60, buffer_minutos]  # cuidado: a duração do novo intervalo é fim - inicio, mas podemos passar diretamente fim_intervalo e usar o buffer. Na segunda condição, precisamos do fim do novo + buffer. Vamos simplificar: usar inicio_intervalo e fim_intervalo.

        # Melhor: a segunda condição: a.data_hora < DATE_ADD(%s, INTERVAL %s MINUTE) onde %s é fim_intervalo e %s é buffer. Mas precisamos da duração do novo? Não, o novo agendamento termina em fim_intervalo, então o buffer após ele é fim_intervalo + buffer. Então a condição é: a.data_hora < fim_intervalo + buffer.
        # Então:
        # AND ( DATE_ADD(a.data_hora, INTERVAL s.duracao_minutos + %s MINUTE) > %s
        #       OR a.data_hora < DATE_ADD(%s, INTERVAL %s MINUTE) )
        # onde o primeiro %s é buffer, segundo %s é inicio_intervalo, terceiro %s é fim_intervalo, quarto %s é buffer.

        params = [profissional_id, buffer_minutos, inicio_intervalo, fim_intervalo, buffer_minutos]

        if ignorar_agendamento_id:
            query += " AND a.id != %s"
            params.append(ignorar_agendamento_id)

        cursor.execute(query, params)
        conflito = cursor.fetchone()
        cursor.close()
        conn.close()
        return conflito is not None
        

    