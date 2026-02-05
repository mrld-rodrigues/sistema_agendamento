from database.connection import get_connection

class ServicoDAO:

    @staticmethod
    def criar(nome, descricao, duracao_minutos, preco):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO servicos (nome, descricao, duracao_minutos, preco)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (nome, descricao, duracao_minutos, preco))
        conn.commit()

        servico_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return servico_id
    
    @staticmethod
    def buscar_por_id(servico_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, duracao_minutos FROM servicos WHERE id = %s",
            (servico_id,)
        )

        servico = cursor.fetchone()

        cursor.close()
        conn.close()

        return servico

