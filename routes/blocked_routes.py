from flask import Blueprint, request, jsonify
from dao.blocked_dao import BloqueioDAO
from datetime import datetime

bloqueios_bp = Blueprint("bloqueios", __name__)


@bloqueios_bp.route("/bloquear-dia", methods=["POST"])
def bloquear_dia():
    data = request.json
    if not data or "profissional_id" not in data or "data" not in data:
        return jsonify({"erro": "profissional_id e data são obrigatórios"}), 400

    try:
        BloqueioDAO.bloquear_dia(
            data["profissional_id"],
            data["data"],
            data.get("motivo")
        )
    except Exception as e:
        return jsonify({"erro": f"Erro ao bloquear dia: {str(e)}"}), 500

    return jsonify({"mensagem": "Dia bloqueado com sucesso"})


@bloqueios_bp.route("/bloquear-horario", methods=["POST"])
def bloquear_horario():
    data = request.json
    campos = ["profissional_id", "data", "hora_inicio", "hora_fim"]
    if not all(c in data for c in campos):
        return jsonify({"erro": f"Campos obrigatórios: {', '.join(campos)}"}), 400

    try:
        BloqueioDAO.bloquear_horario(
            data["profissional_id"],
            data["data"],
            data["hora_inicio"],
            data["hora_fim"],
            data.get("motivo")
        )
    except Exception as e:
        return jsonify({"erro": f"Erro ao bloquear horário: {str(e)}"}), 500

    return jsonify({"mensagem": "Horário bloqueado com sucesso"})


@bloqueios_bp.route("/bloquear-periodo", methods=["POST"])
def bloquear_periodo():
    data = request.json
    campos = ["profissional_id", "data_inicio", "data_fim"]
    if not all(c in data for c in campos):
        return jsonify({"erro": f"Campos obrigatórios: {', '.join(campos)}"}), 400

    try:
        BloqueioDAO.bloquear_periodo(
            data["profissional_id"],
            data["data_inicio"],
            data["data_fim"],
            data.get("motivo")
        )
    except Exception as e:
        return jsonify({"erro": f"Erro ao bloquear período: {str(e)}"}), 500

    return jsonify({"mensagem": "Período bloqueado com sucesso"})


@bloqueios_bp.route("/todos", methods=["GET"])
def listar_todos_bloqueios():
    profissional_id = request.args.get("profissional_id", type=int)
    data = request.args.get("data")

    if not profissional_id:
        return jsonify({"erro": "profissional_id obrigatório"}), 400

    try:
        dados = BloqueioDAO.listar_todos_bloqueios(profissional_id, data)
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar bloqueios: {str(e)}"}), 500

    return jsonify(dados)


@bloqueios_bp.route("/dias-bloqueados", methods=["GET"])
def dias_bloqueados():
    profissional_id = request.args.get("profissional_id", type=int)
    data = request.args.get("data")

    if not profissional_id:
        return jsonify({"erro": "profissional_id obrigatório"}), 400

    try:
        dados = BloqueioDAO.dias_bloqueados(profissional_id, data)
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar dias bloqueados: {str(e)}"}), 500

    return jsonify(dados)


@bloqueios_bp.route("/horarios-bloqueados", methods=["GET"])
def horarios_bloqueados():
    profissional_id = request.args.get("profissional_id", type=int)
    data = request.args.get("data")

    if not profissional_id:
        return jsonify({"erro": "profissional_id obrigatório"}), 400

    try:
        dados = BloqueioDAO.horarios_bloqueados_do_dia(profissional_id, data)
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar horários bloqueados: {str(e)}"}), 500

    return jsonify(dados)


@bloqueios_bp.route("/apagar-dia/<int:bloqueio_id>", methods=["DELETE"])
def apagar_bloqueios_dia(bloqueio_id):
    try:
        sucesso = BloqueioDAO.apagar_bloqueios_dia(bloqueio_id)
    except Exception as e:
        return jsonify({"erro": f"Erro ao deletar bloqueio: {str(e)}"}), 500

    if not sucesso:
        return jsonify({"erro": "Bloqueio não encontrado"}), 404

    return jsonify({"mensagem": "Bloqueio removido"})


@bloqueios_bp.route("/apagar-horario/<int:bloqueio_id>", methods=["DELETE"])
def apagar_bloqueios_horario(bloqueio_id):
    try:
        sucesso = BloqueioDAO.apagar_bloqueios_horario(bloqueio_id)
    except Exception as e:
        return jsonify({"erro": f"Erro ao deletar bloqueio: {str(e)}"}), 500

    if not sucesso:
        return jsonify({"erro": "Bloqueio não encontrado"}), 404

    return jsonify({"mensagem": "Bloqueio removido"})


@bloqueios_bp.route("/recorrente", methods=["POST"])
def criar_bloqueio_recorrente():
    """
    Cria um bloqueio recorrente.
    Corpo JSON:
        profissional_id (int)
        dia_semana (int): 0=segunda, 6=domingo
        hora_inicio (str): "HH:MM"
        hora_fim (str): "HH:MM"
        data_inicio (str, opcional): "YYYY-MM-DD"
        data_fim (str, opcional): "YYYY-MM-DD"
        motivo (str, opcional)
    """
    data = request.json
    campos = ["profissional_id", "dia_semana", "hora_inicio", "hora_fim"]
    if not all(c in data for c in campos):
        return jsonify({"erro": f"Campos obrigatórios: {', '.join(campos)}"}), 400

    try:
        bloqueio_id = BloqueioDAO.criar_bloqueio_recorrente(
            profissional_id=data["profissional_id"],
            dia_semana=data["dia_semana"],
            hora_inicio=data["hora_inicio"],
            hora_fim=data["hora_fim"],
            data_inicio=data.get("data_inicio"),
            data_fim=data.get("data_fim"),
            motivo=data.get("motivo")
        )
    except Exception as e:
        return jsonify({"erro": f"Erro ao criar bloqueio recorrente: {str(e)}"}), 500

    return jsonify({"id": bloqueio_id, "mensagem": "Bloqueio recorrente criado com sucesso"}), 201


@bloqueios_bp.route("/recorrentes", methods=["GET"])
def listar_bloqueios_recorrentes():
    """
    Lista bloqueios recorrentes.
    Parâmetros query:
        profissional_id (opcional): filtrar por profissional
        data (opcional): data de referência (YYYY-MM-DD) para filtrar ativos
    """
    profissional_id = request.args.get("profissional_id", type=int)
    data_ref = request.args.get("data")

    try:
        bloqueios = BloqueioDAO.listar_bloqueios_recorrentes(
            profissional_id=profissional_id,
            data_referencia=data_ref
        )
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar bloqueios recorrentes: {str(e)}"}), 500

    return jsonify(bloqueios), 200


@bloqueios_bp.route("/recorrente/<int:bloqueio_id>", methods=["DELETE"])
def deletar_bloqueio_recorrente(bloqueio_id):
    sucesso = BloqueioDAO.apagar_bloqueio_recorrente(bloqueio_id)
    if not sucesso:
        return jsonify({"erro": "Bloqueio recorrente não encontrado"}), 404
    return jsonify({"mensagem": "Bloqueio recorrente removido com sucesso"}), 200