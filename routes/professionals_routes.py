from flask import Blueprint, request, jsonify
from dao.professional_dao import ProfissionalDAO

profissionais_bp = Blueprint("profissionais", __name__)

# ------------------------------------------------------------
# Rota: POST /profissionais
# Descrição: Cria um novo profissional
# Corpo da requisição (JSON):
#   - nome (obrigatório)
#   - profissao (obrigatório)
#   - email (opcional)
#   - telefone (opcional)
#   - intervalo_minutos (opcional, padrão 15)
# ------------------------------------------------------------
@profissionais_bp.route("", methods=["POST"])
def criar_profissional():
    data = request.get_json()

    # Validação dos campos obrigatórios
    if not data or "nome" not in data or "profissao" not in data:
        return jsonify({"erro": "Os campos 'nome' e 'profissao' são obrigatórios"}), 400

    # Extrai os dados com valores padrão para opcionais
    nome = data["nome"]
    profissao = data["profissao"]
    email = data.get("email")  # None se não existir
    telefone = data.get("telefone")
    intervalo_minutos = data.get("intervalo_minutos", 15)  # padrão 15

    # Chama o DAO para criar o profissional
    try:
        profissional_id = ProfissionalDAO.criar(
            nome=nome,
            profissao=profissao,
            email=email,
            telefone=telefone,
            intervalo_minutos=intervalo_minutos
        )
    except Exception as e:
        # Em caso de erro no banco, retorna 500
        return jsonify({"erro": f"Erro ao criar profissional: {str(e)}"}), 500

    return jsonify({"id": profissional_id, "mensagem": "Profissional criado com sucesso"}), 201


# ------------------------------------------------------------
# Rota: GET /profissionais
# Descrição: Lista todos os profissionais (apenas ativos por padrão)
# Parâmetros de consulta (query string):
#   - incluir_inativos (opcional, se "true" mostra inativos também)
# ------------------------------------------------------------
@profissionais_bp.route("", methods=["GET"])
def listar_profissionais():
    incluir_inativos = request.args.get("incluir_inativos", "false").lower() == "true"
    # Se incluir_inativos for True, passamos False para 'apenas_ativos'
    apenas_ativos = not incluir_inativos

    try:
        profissionais = ProfissionalDAO.listar(apenas_ativos=apenas_ativos)
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar profissionais: {str(e)}"}), 500

    return jsonify(profissionais), 200


# ------------------------------------------------------------
# Rota: GET /profissionais/<int:id>
# Descrição: Retorna os dados de um profissional específico
# ------------------------------------------------------------
@profissionais_bp.route("/<int:id>", methods=["GET"])
def buscar_profissional(id):
    try:
        profissional = ProfissionalDAO.buscar_por_id(id)
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar profissional: {str(e)}"}), 500

    if not profissional:
        return jsonify({"erro": "Profissional não encontrado"}), 404

    return jsonify(profissional), 200


# ------------------------------------------------------------
# Rota: PUT /profissionais/<int:id>
# Descrição: Atualiza parcialmente os dados de um profissional
# Corpo da requisição (JSON): qualquer campo que se deseja alterar
#   (nome, profissao, email, telefone, intervalo_minutos, ativo)
# ------------------------------------------------------------
@profissionais_bp.route("/<int:id>", methods=["PUT"])
def atualizar_profissional(id):
    data = request.get_json()
    if not data:
        return jsonify({"erro": "Nenhum dado enviado para atualização"}), 400

    # Remove chaves vazias ou None se quiser, mas vamos passar tudo que veio
    # O DAO já ignora campos não existentes
    try:
        sucesso = ProfissionalDAO.atualizar(id, data)
    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar profissional: {str(e)}"}), 500

    if not sucesso:
        return jsonify({"erro": "Profissional não encontrado ou nenhuma alteração realizada"}), 404

    return jsonify({"mensagem": "Profissional atualizado com sucesso"}), 200


# ------------------------------------------------------------
# Rota: DELETE /profissionais/<int:id>
# Descrição: Remove (fisicamente) um profissional
# ATENÇÃO: Isso apaga o registro do banco. Se quiser apenas desativar,
#          use a atualização com {"ativo": false}
# ------------------------------------------------------------
@profissionais_bp.route("/<int:id>", methods=["DELETE"])
def deletar_profissional(id):
    try:
        sucesso = ProfissionalDAO.deletar(id)
    except Exception as e:
        return jsonify({"erro": f"Erro ao deletar profissional: {str(e)}"}), 500

    if not sucesso:
        return jsonify({"erro": "Profissional não encontrado"}), 404

    return jsonify({"mensagem": "Profissional deletado com sucesso"}), 200