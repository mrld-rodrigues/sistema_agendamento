from database.connection import get_connection

class ServicoDAO:

    @staticmethod
    def criar(nome, descricao, duracao_minutos, preco, ativo):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO servicos (nome, descricao, duracao_minutos, preco, ativo)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (nome, descricao, duracao_minutos, preco, ativo))
        conn.commit()

        servico_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return servico_id
    
    @staticmethod
    def listar(apenas_ativos=True):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM servicos"
        if apenas_ativos:
            query += " WHERE ativo = 1"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    

    @staticmethod
    def buscar_por_id(servico_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM servicos WHERE id = %s", (servico_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result 
    

    @staticmethod
    def atualizar(servico_id, dados):
        conn = get_connection()
        cursor = conn.cursor()
        fields = []
        values = []
        for key in ['nome', 'descricao', 'duracao_minutos', 'preco', 'ativo']:
            if key in dados:
                fields.append(f"{key} = %s")
                values.append(dados[key])
        if not fields:
            return False
        values.append(servico_id)
        query = f"UPDATE servicos SET {', '.join(fields)} WHERE id = %s"
        cursor.execute(query, values)
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected > 0
    

    @staticmethod
    def deletar(servico_id):
        # Deleção física
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM servicos WHERE id = %s", (servico_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected > 0

