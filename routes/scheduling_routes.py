from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from dao.user_dao import UsuarioDAO
from dao.worktime_dao import HorariosTrabalhoDAO
from dao.blocked_dao import BloqueioDAO
from dao.scheduling_dao import AgendamentoDAO
from services.horarios_livres_services import HorariosLivresService
from dao.service_dao import ServicoDAO
from datetime import datetime

agendamentos_bp = Blueprint("agendamentos", __name__)

@agendamentos_bp.route('', methods=['POST'])
@jwt_required()
def criar_agendamento():
    try:
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        data = request.get_json()
        campos = ['cliente_id', 'profissional_id', 'servico_id', 'data_hora']
        for campo in campos:
            if campo not in data:
                return jsonify({'erro': f'O campo "{campo}" é obrigatório'}), 400

        # Verifica permissão: admin pode criar para qualquer cliente; cliente só para si mesmo
        if usuario['tipo'] == 'admin':
            pass  # autorizado
        elif usuario['tipo'] == 'cliente' and data['cliente_id'] == usuario.get('cliente_id'):
            pass  # autorizado
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        # Converte data_hora
        try:
            data_hora = datetime.fromisoformat(data['data_hora'])
        except ValueError:
            try:
                data_hora = datetime.strptime(data['data_hora'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return jsonify({'erro': 'Formato de data/hora inválido'}), 400

        # Busca serviço para duração
        servico = ServicoDAO.buscar_por_id(data['servico_id'])
        if not servico:
            return jsonify({'erro': 'Serviço não encontrado'}), 404

        # Verifica disponibilidade
        disponivel = HorariosLivresService.verificar_disponibilidade(
            profissional_id=data['profissional_id'],
            data_hora_inicio=data_hora,
            duracao_minutos=servico['duracao_minutos']
        )
        if not disponivel:
            return jsonify({'erro': 'Horário indisponível'}), 409

        agendamento_id = AgendamentoDAO.criar(
            cliente_id=data['cliente_id'],
            profissional_id=data['profissional_id'],
            servico_id=data['servico_id'],
            data_hora=data_hora
        )
        return jsonify({'id': agendamento_id, 'mensagem': 'Agendamento criado com sucesso'}), 201
    except Exception as e:
        print(f"Erro em POST /agendamentos: {str(e)}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500


# Rota de listagem por profissional/data – agora autenticada
@agendamentos_bp.route("", methods=["GET"])
@jwt_required()
def listar_agendamentos():
    try:
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        profissional_id = request.args.get("profissional_id")
        data = request.args.get("data")

        if not profissional_id or not data:
            return jsonify({"erro": "Informe profissional_id e data (YYYY-MM-DD)"}), 400

        # Verifica permissão: admin pode ver qualquer, profissional só seus
        if usuario['tipo'] == 'admin':
            pass
        elif usuario['tipo'] == 'profissional' and int(profissional_id) == usuario.get('profissional_id'):
            pass
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        agendamentos = AgendamentoDAO.listar_por_profissional_e_data(profissional_id, data)
        return jsonify(agendamentos), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar agendamentos: {str(e)}"}), 500


# Rota agenda semanal – autenticada
@agendamentos_bp.route("/semana", methods=["GET"])
@jwt_required()
def agenda_semanal():
    try:
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        profissional_id = request.args.get("profissional_id")
        data_inicio = request.args.get("data_inicio")

        if not profissional_id or not data_inicio:
            return jsonify({"erro": "Informe profissional_id e data_inicio (YYYY-MM-DD)"}), 400

        if usuario['tipo'] == 'admin':
            pass
        elif usuario['tipo'] == 'profissional' and int(profissional_id) == usuario.get('profissional_id'):
            pass
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        agendamentos = AgendamentoDAO.listar_semana(profissional_id, data_inicio)
        return jsonify(agendamentos), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar agenda semanal: {str(e)}"}), 500


# Rota calendário mensal – autenticada
@agendamentos_bp.route("/mes", methods=["GET"])
@jwt_required()
def calendario_mes():
    try:
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        profissional_id = request.args.get("profissional_id")
        ano = request.args.get("ano")
        mes = request.args.get("mes")

        if not profissional_id or not ano or not mes:
            return jsonify({"erro": "Informe profissional_id, ano e mes"}), 400

        if usuario['tipo'] == 'admin':
            pass
        elif usuario['tipo'] == 'profissional' and int(profissional_id) == usuario.get('profissional_id'):
            pass
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        calendario = AgendamentoDAO.calendario_mensal(profissional_id, ano, mes)
        return jsonify(calendario), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao gerar calendário mensal: {str(e)}"}), 500


# Rota calendário completo – autenticada
@agendamentos_bp.route("/mes-completo", methods=["GET"])
@jwt_required()
def calendario_completo():
    try:
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        profissional_id = request.args.get("profissional_id")
        ano = request.args.get("ano")
        mes = request.args.get("mes")

        if not profissional_id or not ano or not mes:
            return jsonify({"erro": "Informe profissional_id, ano e mes"}), 400

        if usuario['tipo'] == 'admin':
            pass
        elif usuario['tipo'] == 'profissional' and int(profissional_id) == usuario.get('profissional_id'):
            pass
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        calendario = AgendamentoDAO.calendario_completo(profissional_id, ano, mes)
        return jsonify(calendario), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao gerar calendário completo: {str(e)}"}), 500


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


@agendamentos_bp.route('/<int:agendamento_id>', methods=['DELETE'])
@jwt_required()
def deletar_agendamento(agendamento_id):
    try:
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        agendamento = AgendamentoDAO.buscar_por_id(agendamento_id)
        if not agendamento:
            return jsonify({'erro': 'Agendamento não encontrado'}), 404

        # Verifica permissão
        if usuario['tipo'] == 'admin':
            pass
        elif usuario['tipo'] == 'profissional' and agendamento['profissional_id'] == usuario.get('profissional_id'):
            pass
        elif usuario['tipo'] == 'cliente' and agendamento['cliente_id'] == usuario.get('cliente_id'):
            pass
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        sucesso = AgendamentoDAO.deletar(agendamento_id)
        if not sucesso:
            return jsonify({'erro': 'Erro ao deletar agendamento'}), 500
        return jsonify({'mensagem': 'Agendamento deletado com sucesso'}), 200
    except Exception as e:
        print(f"Erro em DELETE /agendamentos/{agendamento_id}: {str(e)}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500
