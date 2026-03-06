from database.connection import get_connection

class ClienteDAO:

    @staticmethod
    def criar(nome, email, telefone):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO clientes (nome, email, telefone)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (nome, email, telefone))
        conn.commit()

        cliente_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return cliente_id

    @staticmethod
    def listar():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, nome, email, telefone FROM clientes")
        clientes = cursor.fetchall()

        cursor.close()
        conn.close()

        return clientes
    

    @staticmethod
    def buscar_por_id(cliente_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes WHERE id = %s", (cliente_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def atualizar(cliente_id, dados):
        conn = get_connection()
        cursor = conn.cursor()
        fields = []
        values = []
        for key in ['nome', 'email', 'telefone']:
            if key in dados:
                fields.append(f"{key} = %s")
                values.append(dados[key])
        if not fields:
            return False
        values.append(cliente_id)
        query = f"UPDATE clientes SET {', '.join(fields)} WHERE id = %s"
        cursor.execute(query, values)
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected > 0

    @staticmethod
    def deletar(cliente_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected > 0


    @staticmethod
    def contar():
        """Retorna o número total de clientes cadastrados."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM clientes")
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            cursor.close()
            conn.close()