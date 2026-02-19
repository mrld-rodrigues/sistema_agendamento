from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from dao.service_dao import ServicoDAO
from utils.decorators import admin_required

servicos_bp = Blueprint("servicos", __name__)

# ------------------------------------------------------------
# Rota: POST /servicos
# Descrição: Cria um novo serviço
# Corpo da requisição (JSON):
#   - nome (obrigatório)
#   - descricao (opcional)
#   - duracao_minutos (obrigatório)
#   - preco (obrigatório)
#   - ativo (opcional, padrão True)
# ------------------------------------------------------------
@servicos_bp.route("", methods=["POST"])
@jwt_required()
@admin_required
def criar_servico():
    data = request.get_json()

    # Validação dos campos obrigatórios
    campos_obrigatorios = ["nome", "duracao_minutos", "preco"]
    for campo in campos_obrigatorios:
        if campo not in data:
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400

    # Extrai os dados com valores padrão para opcionais
    nome = data["nome"]
    descricao = data.get("descricao", "")
    duracao_minutos = data["duracao_minutos"]
    preco = data["preco"]
    ativo = data.get("ativo", True)  # padrão True

    # Chama o DAO para criar o serviço
    try:
        servico_id = ServicoDAO.criar(
            nome=nome,
            descricao=descricao,
            duracao_minutos=duracao_minutos,
            preco=preco,
            ativo=ativo
        )
    except Exception as e:
        return jsonify({"erro": f"Erro ao criar serviço: {str(e)}"}), 500

    return jsonify({"id": servico_id, "mensagem": "Serviço criado com sucesso"}), 201


# ------------------------------------------------------------
# Rota: GET /servicos
# Descrição: Lista todos os serviços (apenas ativos por padrão)
# Parâmetros de consulta:
#   - incluir_inativos (opcional, se "true" mostra inativos também)
# ------------------------------------------------------------
@servicos_bp.route("", methods=["GET"])
def listar_servicos():
    incluir_inativos = request.args.get("incluir_inativos", "false").lower() == "true"
    apenas_ativos = not incluir_inativos

    try:
        servicos = ServicoDAO.listar(apenas_ativos=apenas_ativos)
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar serviços: {str(e)}"}), 500

    return jsonify(servicos), 200


# ------------------------------------------------------------
# Rota: GET /servicos/<int:id>
# Descrição: Retorna os dados de um serviço específico
# ------------------------------------------------------------
@servicos_bp.route("/<int:id>", methods=["GET"])
def buscar_servico(id):
    try:
        servico = ServicoDAO.buscar_por_id(id)
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar serviço: {str(e)}"}), 500

    if not servico:
        return jsonify({"erro": "Serviço não encontrado"}), 404

    return jsonify(servico), 200


# ------------------------------------------------------------
# Rota: PUT /servicos/<int:id>
# Descrição: Atualiza parcialmente os dados de um serviço
# Corpo da requisição (JSON): qualquer campo que se deseja alterar
#   (nome, descricao, duracao_minutos, preco, ativo)
# ------------------------------------------------------------
@servicos_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@admin_required
def atualizar_servico(id):
    data = request.get_json()
    if not data:
        return jsonify({"erro": "Nenhum dado enviado para atualização"}), 400

    try:
        sucesso = ServicoDAO.atualizar(id, data)
    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar serviço: {str(e)}"}), 500

    if not sucesso:
        return jsonify({"erro": "Serviço não encontrado ou nenhuma alteração realizada"}), 404

    return jsonify({"mensagem": "Serviço atualizado com sucesso"}), 200


# ------------------------------------------------------------
# Rota: DELETE /servicos/<int:id>
# Descrição: Remove (fisicamente) um serviço
# ATENÇÃO: Isso apaga o registro do banco. Se preferir, pode-se apenas desativar.
# ------------------------------------------------------------
@servicos_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@admin_required
def deletar_servico(id):
    try:
        sucesso = ServicoDAO.deletar(id)
    except Exception as e:
        return jsonify({"erro": f"Erro ao deletar serviço: {str(e)}"}), 500

    if not sucesso:
        return jsonify({"erro": "Serviço não encontrado"}), 404

    return jsonify({"mensagem": "Serviço deletado com sucesso"}), 200