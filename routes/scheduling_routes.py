from flask import Blueprint, request, jsonify
from dao.worktime_dao import HorariosTrabalhoDAO
from dao.blocked_dao import BloqueioDAO
from dao.scheduling_dao import AgendamentoDAO
from services.horarios_livres_services import calcular_horarios_livres
from dao.service_dao import ServicoDAO
from datetime import datetime, timedelta

agendamentos_bp = Blueprint("agendamentos", __name__)

@agendamentos_bp.route("", methods=["POST"])
def criar_agendamento():
    data = request.json

    try:
        data_hora = datetime.fromisoformat(data["data_hora"])
    except ValueError:
        data_hora = datetime.strptime(
            data["data_hora"], "%Y-%m-%d %H:%M:%S"
        )

    # data_hora = datetime.strptime(
    #     data["data_hora"], "%Y-%m-%d %H:%M:%S"
    # )

    servico = ServicoDAO.buscar_por_id(data["servico_id"])

    if not servico:
        return jsonify({"erro": "Serviço não encontrado"}), 404

    conflito = AgendamentoDAO.verificar_conflito(
        data["profissional_id"],
        data_hora,
        servico["duracao_minutos"]
    )

    if conflito:
        return jsonify({
            "erro": "Horário indisponível para este profissional"
        }), 409

    agendamento_id = AgendamentoDAO.criar(
        data["cliente_id"],
        data["profissional_id"],
        data["servico_id"],
        data_hora
    )

    return jsonify({"id": agendamento_id}), 201


@agendamentos_bp.route("", methods=["GET"])
def listar_agendamentos():
    profissional_id = request.args.get("profissional_id")
    data = request.args.get("data")

    if not profissional_id or not data:
        return jsonify({
            "erro": "Informe profissional_id e data (YYYY-MM-DD)"
        }), 400

    agendamentos = AgendamentoDAO.listar_por_profissional_e_data(
        profissional_id,
        data
    )

    return jsonify(agendamentos), 200


@agendamentos_bp.route("/semana", methods=["GET"])
def agenda_semanal():
    profissional_id = request.args.get("profissional_id")
    data_inicio = request.args.get("data_inicio")

    if not profissional_id or not data_inicio:
        return jsonify({
            "erro": "Informe profissional_id e data_inicio (YYYY-MM-DD)"
        }), 400

    agendamentos = AgendamentoDAO.listar_semana(
        profissional_id,
        data_inicio
    )

    return jsonify(agendamentos), 200


@agendamentos_bp.route("/livres", methods=["GET"])
def horarios_livres():
    profissional_id = request.args.get("profissional_id")
    data = request.args.get("data")

    if not profissional_id or not data:
        return jsonify({
            "erro": "Informe profissional_id e data (YYYY-MM-DD)"
        }), 400

    agendados = AgendamentoDAO.buscar_do_dia(
        profissional_id,
        data
    )

    inicio_trabalho = datetime.strptime(f"{data} 18:00:00", "%Y-%m-%d %H:%M:%S")
    fim_trabalho = datetime.strptime(f"{data} 23:59:59", "%Y-%m-%d %H:%M:%S")

    duracao_servico = timedelta(minutes=240)

    livres = []
    atual = inicio_trabalho

    for item in agendados:
        inicio_ocupado = item["data_hora"]
        fim_ocupado = inicio_ocupado + timedelta(
            minutes=item["duracao_minutos"]
        )

        if atual + duracao_servico <= inicio_ocupado:
            livres.append({
                "inicio": atual.strftime("%H:%M"),
                "fim": inicio_ocupado.strftime("%H:%M")
            })

        atual = fim_ocupado

    if atual + duracao_servico <= fim_trabalho:
        livres.append({
            "inicio": atual.strftime("%H:%M"),
            "fim": fim_trabalho.strftime("%H:%M")
        })

    return jsonify(livres), 200


@agendamentos_bp.route("/mes", methods=["GET"])
def calendario_mes():
    profissional_id = request.args.get("profissional_id")
    ano = request.args.get("ano")
    mes = request.args.get("mes")

    if not profissional_id or not ano or not mes:
        return jsonify({
            "erro": "Informe profissional_id, ano e mes"
        }), 400

    calendario = AgendamentoDAO.calendario_mensal(
        profissional_id,
        ano,
        mes
    )

    return jsonify(calendario), 200


@agendamentos_bp.route("/mes-completo", methods=["GET"])
def calendario_completo():
    profissional_id = request.args.get("profissional_id")
    ano = request.args.get("ano")
    mes = request.args.get("mes")

    if not profissional_id or not ano or not mes:
        return jsonify({"erro": "Informe profissional_id, ano e mes"}), 400

    calendario = AgendamentoDAO.calendario_completo(
        profissional_id,
        ano,
        mes
    )

    return jsonify(calendario), 200


@agendamentos_bp.route("/horarios-livres", methods=["GET"])
def listar_horarios_livres():
    profissional_id = request.args.get("profissional_id")
    data_str = request.args.get("data")

    if not profissional_id or not data_str:
        return jsonify({"erro": "Informe profissional_id e data"}), 400

    data = datetime.strptime(data_str, "%Y-%m-%d").date()
    dia_semana = data.weekday()

    jornada = HorariosTrabalhoDAO.buscar_por_profissional_e_dia(
        profissional_id, dia_semana
    )

    agendamentos = AgendamentoDAO.agendamentos_do_dia(
        profissional_id, data
    )

    bloqueios = BloqueioDAO.bloqueios_do_dia(
        profissional_id, data
    )

    livres = calcular_horarios_livres(
        jornada, agendamentos, bloqueios, data
    )

    resposta = [
        {
            "inicio": l[0].strftime("%H:%M"),
            "fim": l[1].strftime("%H:%M")
        }
        for l in livres
    ]

    return jsonify(resposta), 200
