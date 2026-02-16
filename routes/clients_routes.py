from flask import Blueprint, request, jsonify
from dao.client_dao import ClienteDAO

clientes_bp = Blueprint("clientes", __name__)

@clientes_bp.route("", methods=["POST"])
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
def listar_clientes():
    try:
        clientes = ClienteDAO.listar()
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar clientes: {str(e)}"}), 500
    return jsonify(clientes), 200


@clientes_bp.route("/<int:id>", methods=["GET"])
def buscar_cliente(id):
    try:
        cliente = ClienteDAO.buscar_por_id(id)
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar cliente: {str(e)}"}), 500
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    return jsonify(cliente), 200


@clientes_bp.route("/<int:id>", methods=["PUT"])
def atualizar_cliente(id):
    data = request.json
    if not data:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    try:
        sucesso = ClienteDAO.atualizar(id, data)
    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar cliente: {str(e)}"}), 500

    if not sucesso:
        return jsonify({"erro": "Cliente não encontrado ou nenhuma alteração"}), 404

    return jsonify({"mensagem": "Cliente atualizado com sucesso"}), 200


@clientes_bp.route("/<int:id>", methods=["DELETE"])
def deletar_cliente(id):
    try:
        sucesso = ClienteDAO.deletar(id)
    except Exception as e:
        return jsonify({"erro": f"Erro ao deletar cliente: {str(e)}"}), 500

    if not sucesso:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    return jsonify({"mensagem": "Cliente deletado com sucesso"}), 200
