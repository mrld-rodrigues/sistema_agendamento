from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from dao.client_dao import ClienteDAO
from dao.user_dao import UsuarioDAO
from utils.decorators import admin_required

clientes_bp = Blueprint("clientes", __name__)

@clientes_bp.route("", methods=["POST"])
@jwt_required()
# @admin_required
def criar_cliente():
    data = request.json
    if not data or "nome" not in data:
        return jsonify({"erro": "O campo 'nome' é obrigatório"}), 400

    try:
        cliente_id = ClienteDAO.criar(
            data["nome"],
            data.get("email"),
            data.get("telefone")
        )
    except Exception as e:
        return jsonify({"erro": f"Erro ao criar cliente: {str(e)}"}), 500

    return jsonify({"id": cliente_id}), 201


@clientes_bp.route("", methods=["GET"])
@jwt_required()
@admin_required
def listar_clientes():
    try:
        clientes = ClienteDAO.listar()
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar clientes: {str(e)}"}), 500
    return jsonify(clientes), 200


@clientes_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def buscar_cliente(id):
    try:
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        # Verifica permissões
        if usuario['tipo'] == 'admin':
            cliente = ClienteDAO.buscar_por_id(id)
        elif usuario['tipo'] == 'cliente' and usuario.get('cliente_id') == id:
            cliente = ClienteDAO.buscar_por_id(id)
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        if not cliente:
            return jsonify({'erro': 'Cliente não encontrado'}), 404

        return jsonify(cliente), 200

    except Exception as e:
        # Log do erro (opcional, mas recomendado)
        print(f"Erro ao buscar cliente: {str(e)}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500


@clientes_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_cliente(id):
    try:
        # 1. Obtém o usuário logado
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        # 2. Verifica permissão
        # Admin pode atualizar qualquer cliente; cliente só pode atualizar a si mesmo
        if usuario['tipo'] == 'admin':
            pass  # autorizado
        elif usuario['tipo'] == 'cliente' and usuario.get('cliente_id') == id:
            pass  # autorizado
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        # 3. Valida o corpo da requisição
        data = request.get_json()
        if not data:
            return jsonify({'erro': 'Nenhum dado enviado para atualização'}), 400

        # (Opcional) Verificar se há pelo menos um campo válido
        campos_permitidos = ['nome', 'email', 'telefone']
        if not any(campo in data for campo in campos_permitidos):
            return jsonify({'erro': 'Nenhum campo válido para atualização'}), 400

        # 4. Tenta atualizar no banco
        sucesso = ClienteDAO.atualizar(id, data)

        if not sucesso:
            # Pode ser que o cliente não exista ou nenhum campo foi alterado
            return jsonify({'erro': 'Cliente não encontrado ou nenhuma alteração realizada'}), 404

        return jsonify({'mensagem': 'Cliente atualizado com sucesso'}), 200

    except Exception as e:
        # 5. Tratamento de exceções inesperadas
        # Em produção, você pode logar o erro (e) em um arquivo de log
        print(f"Erro ao atualizar cliente: {str(e)}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500


@clientes_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@admin_required
def deletar_cliente(id):
    try:
        sucesso = ClienteDAO.deletar(id)
    except Exception as e:
        return jsonify({"erro": f"Erro ao deletar cliente: {str(e)}"}), 500

    if not sucesso:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    return jsonify({"mensagem": "Cliente deletado com sucesso"}), 200
