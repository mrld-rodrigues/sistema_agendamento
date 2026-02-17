from database.connection import get_connection
import bcrypt

class UsuarioDAO:

    @staticmethod
    def criar(email, senha, tipo, profissional_id=None, cliente_id=None):
        """Cria um novo usuário com senha hasheada."""
        # Hash da senha
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (email, senha_hash, tipo, profissional_id, cliente_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (email, senha_hash, tipo, profissional_id, cliente_id))
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return user_id

    @staticmethod
    def buscar_por_email(email):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def buscar_por_id(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def autenticar(email, senha):
        """Retorna o usuário se a senha estiver correta, senão None."""
        user = UsuarioDAO.buscar_por_email(email)
        if user and bcrypt.checkpw(senha.encode('utf-8'), user['senha_hash'].encode('utf-8')):
            return user
        return None

    @staticmethod
    def atualizar(user_id, dados):
        """Atualiza campos do usuário (ex.: ativo, email, senha)."""
        conn = get_connection()
        cursor = conn.cursor()
        campos = []
        valores = []
        if 'email' in dados:
            campos.append("email = %s")
            valores.append(dados['email'])
        if 'senha' in dados:
            # Se for alterar a senha, recebemos a nova senha em texto plano e hasheamos
            salt = bcrypt.gensalt()
            senha_hash = bcrypt.hashpw(dados['senha'].encode('utf-8'), salt).decode('utf-8')
            campos.append("senha_hash = %s")
            valores.append(senha_hash)
        if 'ativo' in dados:
            campos.append("ativo = %s")
            valores.append(dados['ativo'])
        if not campos:
            return False
        valores.append(user_id)
        query = f"UPDATE usuarios SET {', '.join(campos)} WHERE id = %s"
        cursor.execute(query, valores)
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected > 0