from flask import Blueprint, request, jsonify
from dao.scheduling_dao import AgendamentoDAO
from dao.blocked_dao import BloqueioDAO

from datetime import datetime

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/agendamentos", methods=["GET"])
def listar_agendamentos():
    data = request.args.get("data")
    profissional_id = request.args.get("profissional_id")

    agendamentos = AgendamentoDAO.listar(
        data=data,
        profissional_id=profissional_id
    )

    return jsonify(agendamentos)


@admin_bp.route("/agendamentos/<int:id>/remarcar", methods=["PUT"])
def remarcar_agendamento(id):
    dados = request.json
    nova_data = datetime.strptime(
        dados["data_hora"], "%Y-%m-%d %H:%M:%S"
    )

    sucesso = AgendamentoDAO.remarcar(id, nova_data)

    if not sucesso:
        return jsonify({"erro": "Agendamento não encontrado"}), 404

    return jsonify({"mensagem": "Agendamento remarcado com sucesso"})


@admin_bp.route("/agenda", methods=["GET"])
def agenda_profissional():
    profissional_id = request.args.get("profissional_id", type=int)
    data = request.args.get("data")  # YYYY-MM-DD

    if not profissional_id or not data:
        return jsonify({"erro": "Informe profissional_id e data"}), 400

    data_obj = datetime.strptime(data, "%Y-%m-%d").date()

    agendamentos = AgendamentoDAO.listar_por_profissional_e_data(
        profissional_id,
        data_obj
    )

    return jsonify(agendamentos)


@admin_bp.route("/agendamentos/<int:agendamento_id>", methods=["DELETE"])
def deletar_agendamento(agendamento_id):

    sucesso = AgendamentoDAO.deletar(agendamento_id)

    if not sucesso:
        return jsonify({"erro": "Agendamento não encontrado"}), 404

    return jsonify({"mensagem": "Agendamento deletado com sucesso"})


@admin_bp.route("/bloquear-dia", methods=["POST"])
def bloquear_dia():

    data = request.json

    BloqueioDAO.bloquear_dia(
        data["profissional_id"],
        data["data"],
        data.get("motivo")
    )

    return jsonify({"mensagem": "Dia bloqueado com sucesso"})


@admin_bp.route("/bloquear-horario", methods=["POST"])
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


@admin_bp.route("/bloquear-periodo", methods=["POST"])
def bloquear_periodo():

    data = request.json

    BloqueioDAO.bloquear_periodo(
        data["profissional_id"],
        data["data_inicio"],
        data["data_fim"],
        data.get("motivo")
    )

    return jsonify({"mensagem": "Período bloqueado com sucesso"})




    