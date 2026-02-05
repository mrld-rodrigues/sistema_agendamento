from flask import Blueprint, request, jsonify
from dao.service_dao import ServicoDAO

servicos_bp = Blueprint("servicos", __name__)

@servicos_bp.route("", methods=["POST"])
def criar_servico():
    data = request.json

    servico_id = ServicoDAO.criar(
        data["nome"],
        data["descricao"],
        data["duracao_minutos"],
        data["preco"]
    )

    return jsonify({"id": servico_id}), 201
