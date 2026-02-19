from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from dao.user_dao import UsuarioDAO
from dao.client_dao import ClienteDAO
from dao.professional_dao import ProfissionalDAO

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    if not dados or 'email' not in dados or 'senha' not in dados:
        return jsonify({'erro': 'Email e senha são obrigatórios'}), 400

    usuario = UsuarioDAO.autenticar(dados['email'], dados['senha'])
    if not usuario:
        return jsonify({'erro': 'Credenciais inválidas'}), 401

    if not usuario['ativo']:
        return jsonify({'erro': 'Usuário inativo'}), 403

    # Criar token com identidade = id do usuário
    access_token = create_access_token(identity=str(usuario['id']))
    return jsonify({
        'access_token': access_token,
        'tipo': usuario['tipo']
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    usuario = UsuarioDAO.buscar_por_id(user_id)
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    # Remove hash antes de retornar
    usuario.pop('senha_hash', None)
    return jsonify(usuario), 200

# Rota para registrar um novo cliente (cria cliente e usuário)
@auth_bp.route('/registro/cliente', methods=['POST'])
def registro_cliente():
    dados = request.get_json()
    campos = ['nome', 'email', 'senha']
    if not all(c in dados for c in campos):
        return jsonify({'erro': 'Campos obrigatórios: nome, email, senha'}), 400

    # Verificar se email já existe como usuário
    if UsuarioDAO.buscar_por_email(dados['email']):
        return jsonify({'erro': 'Email já cadastrado'}), 409

    # Criar cliente
    try:
        cliente_id = ClienteDAO.criar(dados['nome'], dados['email'], dados.get('telefone'))
    except Exception as e:
        return jsonify({'erro': f'Erro ao criar cliente: {str(e)}'}), 500

    # Criar usuário vinculado
    try:
        usuario_id = UsuarioDAO.criar(
            email=dados['email'],
            senha=dados['senha'],
            tipo='cliente',
            cliente_id=cliente_id
        )
    except Exception as e:
        # Se falhar, podemos tentar reverter a criação do cliente? Ou apenas retornar erro.
        return jsonify({'erro': f'Erro ao criar usuário: {str(e)}'}), 500

    return jsonify({
        'cliente_id': cliente_id,
        'usuario_id': usuario_id,
        'mensagem': 'Cliente registrado com sucesso'
    }), 201

# Rota para registrar um profissional (apenas admin pode criar?)
@auth_bp.route('/registro/profissional', methods=['POST'])
def registro_profissional():
    # Idealmente, apenas admin pode criar profissional. Mas vamos simplificar por enquanto.
    dados = request.get_json()
    campos = ['nome', 'especialidade', 'email', 'senha']
    if not all(c in dados for c in campos):
        return jsonify({'erro': 'Campos obrigatórios: nome, especialidade, email, senha'}), 400

    if UsuarioDAO.buscar_por_email(dados['email']):
        return jsonify({'erro': 'Email já cadastrado'}), 409

    try:
        profissional_id = ProfissionalDAO.criar(
            nome=dados['nome'],
            especialidade=dados['especialidade'],
            email=dados['email'],
            telefone=dados.get('telefone'),
            intervalo_minutos=dados.get('intervalo_minutos', 15)
        )
    except Exception as e:
        return jsonify({'erro': f'Erro ao criar profissional: {str(e)}'}), 500

    try:
        usuario_id = UsuarioDAO.criar(
            email=dados['email'],
            senha=dados['senha'],
            tipo='profissional',
            profissional_id=profissional_id
        )
    except Exception as e:
        return jsonify({'erro': f'Erro ao criar usuário: {str(e)}'}), 500

    return jsonify({
        'profissional_id': profissional_id,
        'usuario_id': usuario_id,
        'mensagem': 'Profissional registrado com sucesso'
    }), 201