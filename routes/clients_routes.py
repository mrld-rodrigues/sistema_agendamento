from flask import Blueprint, request, jsonify
from dao.client_dao import ClienteDAO

clientes_bp = Blueprint("clientes", __name__)

@clientes_bp.route("", methods=["POST"])
def criar_cliente():
    data = request.json

    cliente_id = ClienteDAO.criar(
        data["nome"],
        data["email"],
        data["telefone"]
    )

    return jsonify({"id": cliente_id}), 201


@clientes_bp.route("", methods=["GET"])
def listar_clientes():
    clientes = ClienteDAO.listar()
    return jsonify(clientes), 200
