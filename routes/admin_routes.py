from flask import Blueprint, request, jsonify
from dao.scheduling_dao import AgendamentoDAO
from dao.blocked_dao import BloqueioDAO
from datetime import datetime
from services.horarios_livres_services import HorariosLivresService
from utils.decorators import admin_required
from flask_jwt_extended import jwt_required

admin_bp = Blueprint("admin", __name__)


# -------------------- AGENDAMENTOS --------------------
@admin_bp.route("/agendamentos", methods=["GET"])
@jwt_required()
@admin_required
def listar_agendamentos():
    try:
        data = request.args.get("data")
        profissional_id = request.args.get("profissional_id")
        agendamentos = AgendamentoDAO.listar(data=data, profissional_id=profissional_id)
        return jsonify(agendamentos)
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar agendamentos: {str(e)}"}), 500


@admin_bp.route("/agendamentos/<int:id>/remarcar", methods=["PUT"])
@jwt_required()
@admin_required
def remarcar_agendamento(id):
    try:
        dados = request.get_json()
        if not dados or "data_hora" not in dados:
            return jsonify({"erro": "O campo 'data_hora' é obrigatório"}), 400

        # Converter nova data/hora
        try:
            nova_data = datetime.fromisoformat(dados["data_hora"])
        except ValueError:
            try:
                nova_data = datetime.strptime(dados["data_hora"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return jsonify({"erro": "Formato de data/hora inválido. Use ISO ou YYYY-MM-DD HH:MM:SS"}), 400

        # Buscar o agendamento original
        agendamento = AgendamentoDAO.buscar_por_id(id)
        if not agendamento:
            return jsonify({"erro": "Agendamento não encontrado"}), 404

        # Verificar disponibilidade
        disponivel = HorariosLivresService.verificar_disponibilidade(
            profissional_id=agendamento["profissional_id"],
            data_hora_inicio=nova_data,
            duracao_minutos=agendamento["duracao_minutos"],
            ignorar_agendamento_id=id
        )
        if not disponivel:
            return jsonify({"erro": "Horário indisponível para este profissional"}), 409

        sucesso = AgendamentoDAO.remarcar(id, nova_data)
        if not sucesso:
            return jsonify({"erro": "Falha ao remarcar agendamento"}), 500

        return jsonify({"mensagem": "Agendamento remarcado com sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500


@admin_bp.route("/agenda", methods=["GET"])
@jwt_required()
@admin_required
def agenda_profissional():
    try:
        profissional_id = request.args.get("profissional_id", type=int)
        data = request.args.get("data")
        if not profissional_id or not data:
            return jsonify({"erro": "Informe profissional_id e data"}), 400

        data_obj = datetime.strptime(data, "%Y-%m-%d").date()
        agendamentos = AgendamentoDAO.listar_por_profissional_e_data(profissional_id, data_obj)
        return jsonify(agendamentos)
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar agenda: {str(e)}"}), 500


@admin_bp.route("/agendamentos/<int:agendamento_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def deletar_agendamento(agendamento_id):
    try:
        sucesso = AgendamentoDAO.deletar(agendamento_id)
        if not sucesso:
            return jsonify({"erro": "Agendamento não encontrado"}), 404
        return jsonify({"mensagem": "Agendamento deletado com sucesso"})
    except Exception as e:
        return jsonify({"erro": f"Erro ao deletar agendamento: {str(e)}"}), 500


# -------------------- BLOQUEIOS --------------------
@admin_bp.route("/bloquear-dia", methods=["POST"])
@jwt_required()
@admin_required
def bloquear_dia():
    try:
        data = request.json
        if not data or "profissional_id" not in data or "data" not in data:
            return jsonify({"erro": "profissional_id e data são obrigatórios"}), 400
        BloqueioDAO.bloquear_dia(data["profissional_id"], data["data"], data.get("motivo"))
        return jsonify({"mensagem": "Dia bloqueado com sucesso"})
    except Exception as e:
        return jsonify({"erro": f"Erro ao bloquear dia: {str(e)}"}), 500


@admin_bp.route("/bloquear-horario", methods=["POST"])
@jwt_required()
@admin_required
def bloquear_horario():
    try:
        data = request.json
        campos = ["profissional_id", "data", "hora_inicio", "hora_fim"]
        if not all(c in data for c in campos):
            return jsonify({"erro": f"Campos obrigatórios: {', '.join(campos)}"}), 400
        BloqueioDAO.bloquear_horario(
            data["profissional_id"],
            data["data"],
            data["hora_inicio"],
            data["hora_fim"],
            data.get("motivo")
        )
        return jsonify({"mensagem": "Horário bloqueado com sucesso"})
    except Exception as e:
        return jsonify({"erro": f"Erro ao bloquear horário: {str(e)}"}), 500


@admin_bp.route("/bloquear-periodo", methods=["POST"])
@jwt_required()
@admin_required
def bloquear_periodo():
    try:
        data = request.json
        campos = ["profissional_id", "data_inicio", "data_fim"]
        if not all(c in data for c in campos):
            return jsonify({"erro": f"Campos obrigatórios: {', '.join(campos)}"}), 400
        BloqueioDAO.bloquear_periodo(
            data["profissional_id"],
            data["data_inicio"],
            data["data_fim"],
            data.get("motivo")
        )
        return jsonify({"mensagem": "Período bloqueado com sucesso"})
    except Exception as e:
        return jsonify({"erro": f"Erro ao bloquear período: {str(e)}"}), 500


@admin_bp.route("/bloqueios", methods=["GET"])
@jwt_required()
@admin_required
def listar_bloqueios_admin():
    try:
        profissional_id = request.args.get("profissional_id", type=int)
        data = request.args.get("data")
        if not profissional_id:
            return jsonify({"erro": "profissional_id obrigatório"}), 400
        dados = BloqueioDAO.listar_todos_bloqueios(profissional_id, data)
        return jsonify(dados)
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar bloqueios: {str(e)}"}), 500


@admin_bp.route("/bloqueios/<int:bloqueio_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def apagar_bloqueio_dia_admin(bloqueio_id):
    try:
        sucesso = BloqueioDAO.apagar_bloqueios_dia(bloqueio_id)
        if not sucesso:
            return jsonify({"erro": "Bloqueio não encontrado"}), 404
        return jsonify({"mensagem": "Bloqueio removido com sucesso"})
    except Exception as e:
        return jsonify({"erro": f"Erro ao deletar bloqueio: {str(e)}"}), 500


@admin_bp.route("/bloqueios/horario/<int:bloqueio_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def apagar_bloqueio_horario_admin(bloqueio_id):
    try:
        sucesso = BloqueioDAO.apagar_bloqueios_horario(bloqueio_id)
        if not sucesso:
            return jsonify({"erro": "Bloqueio não encontrado"}), 404
        return jsonify({"mensagem": "Bloqueio removido com sucesso"})
    except Exception as e:
        return jsonify({"erro": f"Erro ao deletar bloqueio: {str(e)}"}), 500


@admin_bp.route("/bloqueios/recorrente", methods=["POST"])
@jwt_required()
@admin_required
def admin_criar_bloqueio_recorrente():
    try:
        data = request.json
        campos = ["profissional_id", "dia_semana", "hora_inicio", "hora_fim"]
        if not all(c in data for c in campos):
            return jsonify({"erro": f"Campos obrigatórios: {', '.join(campos)}"}), 400
        bloqueio_id = BloqueioDAO.criar_bloqueio_recorrente(
            profissional_id=data["profissional_id"],
            dia_semana=data["dia_semana"],
            hora_inicio=data["hora_inicio"],
            hora_fim=data["hora_fim"],
            data_inicio=data.get("data_inicio"),
            data_fim=data.get("data_fim"),
            motivo=data.get("motivo")
        )
        return jsonify({"id": bloqueio_id, "mensagem": "Bloqueio recorrente criado com sucesso"}), 201
    except Exception as e:
        return jsonify({"erro": f"Erro ao criar bloqueio recorrente: {str(e)}"}), 500


@admin_bp.route("/bloqueios/recorrentes", methods=["GET"])
@jwt_required()
@admin_required
def admin_listar_bloqueios_recorrentes():
    try:
        profissional_id = request.args.get("profissional_id", type=int)
        data_ref = request.args.get("data")
        bloqueios = BloqueioDAO.listar_bloqueios_recorrentes(
            profissional_id=profissional_id,
            data_referencia=data_ref
        )
        return jsonify(bloqueios), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar bloqueios recorrentes: {str(e)}"}), 500


@admin_bp.route("/bloqueios/recorrente/<int:bloqueio_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def admin_deletar_bloqueio_recorrente(bloqueio_id):
    try:
        sucesso = BloqueioDAO.apagar_bloqueio_recorrente(bloqueio_id)
        if not sucesso:
            return jsonify({"erro": "Bloqueio recorrente não encontrado"}), 404
        return jsonify({"mensagem": "Bloqueio recorrente removido com sucesso"})
    except Exception as e:
        return jsonify({"erro": f"Erro ao deletar bloqueio recorrente: {str(e)}"}), 500