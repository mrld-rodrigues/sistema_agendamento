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


@bloqueios_bp.route("/todos", methods=["GET"])
def listar_todos_bloqueios():
    profissional_id = request.args.get("profissional_id", type=int)
    data = request.args.get("data")

    if not profissional_id:
        return jsonify({"erro": "profissional_id obrigatório"}), 400

    dados = BloqueioDAO.listar_todos_bloqueios(profissional_id, data)

    return jsonify(dados)


@bloqueios_bp.route("/dias-bloqueados", methods=["GET"])
def dias_bloqueados():
    profissional_id = request.args.get("profissional_id", type=int)
    data = request.args.get("data")

    if not profissional_id:
        return jsonify({"erro": "profissional_id obrigatório"}), 400

    dados = BloqueioDAO.dias_bloqueados(profissional_id, data)

    return jsonify(dados)


@bloqueios_bp.route("/dia", methods=["GET"])
def bloqueios_do_dia():
    profissional_id = request.args.get("profissional_id", type=int)
    data = request.args.get("data")

    dados = BloqueioDAO.bloqueios_do_dia(profissional_id, data)

    return jsonify(dados)


@bloqueios_bp.route("/apagar-dia/<int:bloqueio_id>", methods=["DELETE"])
def apagar_bloqueios_dia(bloqueio_id):
    sucesso = BloqueioDAO.apagar_bloqueios_dia(bloqueio_id)

    if not sucesso:
        return jsonify({"erro": "Bloqueio não encontrado"}), 404

    return jsonify({"mensagem": "Bloqueio removido"})


@bloqueios_bp.route("/apagar-horario/<int:bloqueio_id>", methods=["DELETE"])
def apagar_bloqueios_horario(bloqueio_id):
    sucesso = BloqueioDAO.apagar_bloqueios_horario(bloqueio_id)

    if not sucesso:
        return jsonify({"erro": "Bloqueio não encontrado"}), 404

    return jsonify({"mensagem": "Bloqueio removido"})