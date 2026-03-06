from database.connection import get_connection

class ProfissionalDAO:
    @staticmethod
    def criar(nome, especialidade, email=None, telefone=None, intervalo_minutos=15):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO profissionais (nome, especialidade, email, telefone, intervalo_minutos)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nome, especialidade, email, telefone, intervalo_minutos))
        conn.commit()
        prof_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return prof_id


    @staticmethod
    def listar(apenas_ativos=True):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM profissionais"
        if apenas_ativos:
            query += " WHERE ativo = 1"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    

    @staticmethod
    def buscar_por_id(profissional_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM profissionais WHERE id = %s", (profissional_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def atualizar(profissional_id, dados):
        # dados pode conter nome, especialidade, email, telefone, intervalo_minutos, ativo
        conn = get_connection()
        cursor = conn.cursor()
        fields = []
        values = []
        for key in ['nome', 'especialidade', 'email', 'telefone', 'intervalo_minutos', 'ativo']:
            if key in dados:
                fields.append(f"{key} = %s")
                values.append(dados[key])
        if not fields:
            return False
        values.append(profissional_id)
        query = f"UPDATE profissionais SET {', '.join(fields)} WHERE id = %s"
        cursor.execute(query, values)
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected > 0
    

    @staticmethod
    def deletar(profissional_id):
        # Aqui podemos optar por deleção lógica (set ativo=0) ou física.
        # Vamos manter física por enquanto, mas o ideal é lógica.
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM profissionais WHERE id = %s", (profissional_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected > 0
    

    @staticmethod
    def contar_ativos():
        """Retorna o número de profissionais com ativo = 1."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM profissionais WHERE ativo = 1")
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            cursor.close()
            conn.close()