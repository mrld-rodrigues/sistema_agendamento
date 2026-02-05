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
