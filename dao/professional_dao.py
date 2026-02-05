from database.connection import get_connection

class ProfissionalDAO:

    @staticmethod
    def criar(nome, email, telefone, especialidade):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO profissionais (nome, email, telefone, especialidade)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (nome, email, telefone, especialidade))
        conn.commit()

        profissional_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return profissional_id
