from flask import Blueprint, request, jsonify
from dao.professional_dao import ProfissionalDAO

profissionais_bp = Blueprint("profissionais", __name__)

@profissionais_bp.route("", methods=["POST"])
def criar_profissional():
    data = request.json

    profissional_id = ProfissionalDAO.criar(
        data["nome"],
        data["email"],
        data["telefone"],
        data["especialidade"]
    )

    return jsonify({"id": profissional_id}), 201
