from flask import Blueprint, request, jsonify
from dao.blocked_dao import BloqueioDAO
from datetime import datetime

bloqueios_bp = Blueprint("bloqueios", __name__)


@bloqueios_bp.route("/bloquear-dia", methods=["POST"])
def bloquear_dia():

    data = request.json

    BloqueioDAO.bloquear_dia(
        data["profissional_id"],
        data["data"],
        data.get("motivo")
    )

    return jsonify({"mensagem": "Dia bloqueado com sucesso"})


@bloqueios_bp.route("/bloquear-horario", methods=["POST"])
def bloquear_horario():

    data = request.json

    BloqueioDAO.bloquear_horario(
        data["profissional_id"],
        data["data"],
        data["hora_inicio"],
        data["hora_fim"],
        data.get("motivo")
    )

    return jsonify({"mensagem": "Horário bloqueado com sucesso"})


@bloqueios_bp.route("/bloquear-periodo", methods=["POST"])
def bloquear_periodo():

    data = request.json

    BloqueioDAO.bloquear_periodo(
        data["profissional_id"],
        data["data_inicio"],
        data["data_fim"],
        data.get("motivo")
    )

    return jsonify({"mensagem": "Período bloqueado com sucesso"})


@bloqueios_bp.route("/bloqueios", methods=["GET"])
def listar_bloqueios():
    profissional_id = request.args.get("profissional_id", type=int)
    data = request.args.get("data")

    if not profissional_id:
        return jsonify({"erro": "profissional_id obrigatório"}), 400

    dados = BloqueioDAO.listar_bloqueios(profissional_id, data)

    return jsonify(dados)


@bloqueios_bp.route("/bloqueios/<int:bloqueio_id>", methods=["DELETE"])
def deletar_bloqueio(bloqueio_id):
    sucesso = BloqueioDAO.apagar_bloqueios(bloqueio_id)

    if not sucesso:
        return jsonify({"erro": "Bloqueio não encontrado"}), 404

    return jsonify({"mensagem": "Bloqueio removido"})