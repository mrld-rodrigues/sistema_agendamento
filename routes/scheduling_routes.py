from flask import Blueprint, request, jsonify
from dao.worktime_dao import HorariosTrabalhoDAO
from dao.blocked_dao import BloqueioDAO
from dao.scheduling_dao import AgendamentoDAO
from services.horarios_livres_services import HorariosLivresService
from dao.service_dao import ServicoDAO
from datetime import datetime, timedelta

agendamentos_bp = Blueprint("agendamentos", __name__)

@agendamentos_bp.route("", methods=["POST"])
def criar_agendamento():
    data = request.json

    # Validar campos obrigatórios
    campos = ["cliente_id", "profissional_id", "servico_id", "data_hora"]
    if not all(c in data for c in campos):
        return jsonify({"erro": "Campos obrigatórios: " + ", ".join(campos)}), 400

    # Converter data_hora para datetime
    try:
        data_hora = datetime.fromisoformat(data["data_hora"])
    except ValueError:
        try:
            data_hora = datetime.strptime(data["data_hora"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify({"erro": "Formato de data/hora inválido. Use ISO ou YYYY-MM-DD HH:MM:SS"}), 400

    # Buscar serviço
    servico = ServicoDAO.buscar_por_id(data["servico_id"])
    if not servico:
        return jsonify({"erro": "Serviço não encontrado"}), 404

    # Verificar disponibilidade usando o serviço
    try:
        disponivel = HorariosLivresService.verificar_disponibilidade(
            profissional_id=data["profissional_id"],
            data_hora_inicio=data_hora,
            duracao_minutos=servico["duracao_minutos"]
        )
    except Exception as e:
        return jsonify({"erro": f"Erro ao verificar disponibilidade: {str(e)}"}), 500

    if not disponivel:
        return jsonify({"erro": "Horário indisponível para este profissional (conflito com agendamento ou bloqueio)"}), 409

    # Criar agendamento
    try:
        agendamento_id = AgendamentoDAO.criar(
            cliente_id=data["cliente_id"],
            profissional_id=data["profissional_id"],
            servico_id=data["servico_id"],
            data_hora=data_hora
        )
    except Exception as e:
        return jsonify({"erro": f"Erro ao criar agendamento: {str(e)}"}), 500

    return jsonify({"id": agendamento_id, "mensagem": "Agendamento criado com sucesso"}), 201


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
    """
    Retorna os horários livres para um profissional em uma determinada data.
    
    Parâmetros de consulta (query string):
        profissional_id (obrigatório): ID do profissional
        data (obrigatório): data no formato YYYY-MM-DD
        servico_id (opcional): ID do serviço (para obter a duração)
        duracao (opcional): duração em minutos (usado se servico_id não for informado)
    
    Retorno:
        Lista de intervalos com formato {"inicio": "HH:MM", "fim": "HH:MM"}
    """
    # Extrair parâmetros da query string
    profissional_id = request.args.get("profissional_id", type=int)
    data_str = request.args.get("data")
    servico_id = request.args.get("servico_id", type=int)
    duracao = request.args.get("duracao", type=int)

    # Validações básicas
    if not profissional_id or not data_str:
        return jsonify({"erro": "Informe profissional_id e data (formato YYYY-MM-DD)"}), 400

    # Converter data
    try:
        data = datetime.strptime(data_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"erro": "Formato de data inválido. Use YYYY-MM-DD"}), 400

    # Determinar a duração necessária
    duracao_necessaria = None
    if servico_id:
        # Buscar serviço para obter duração
        servico = ServicoDAO.buscar_por_id(servico_id)
        if not servico:
            return jsonify({"erro": "Serviço não encontrado"}), 404
        duracao_necessaria = servico["duracao_minutos"]
    elif duracao:
        duracao_necessaria = duracao

    # Calcular horários livres usando o serviço
    try:
        intervalos = HorariosLivresService.calcular_horarios_livres(
            profissional_id=profissional_id,
            data=data,
            duracao_necessaria=duracao_necessaria
        )
    except Exception as e:
        return jsonify({"erro": f"Erro ao calcular horários livres: {str(e)}"}), 500

    # Formatar resposta
    resposta = [
        {
            "inicio": inicio.strftime("%H:%M"),
            "fim": fim.strftime("%H:%M")
        }
        for inicio, fim in intervalos
    ]

    return jsonify(resposta), 200
