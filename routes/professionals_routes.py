from datetime import date, datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from dao.blocked_dao import BloqueioDAO
from dao.professional_dao import ProfissionalDAO
from dao.user_dao import UsuarioDAO
from utils.decorators import admin_required


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
@jwt_required()
@admin_required
def criar_profissional():
    data = request.get_json()

    # Validação dos campos obrigatórios
    if not data or "nome" not in data or "especialidade" not in data:
        return jsonify({"erro": "Os campos 'nome' e 'especialidade' são obrigatórios"}), 400

    # Extrai os dados com valores padrão para opcionais
    nome = data["nome"]
    especialidade = data["especialidade"]
    email = data.get("email")  # None se não existir
    telefone = data.get("telefone")
    intervalo_minutos = data.get("intervalo_minutos", 15)  # padrão 15

    # Chama o DAO para criar o profissional
    try:
        profissional_id = ProfissionalDAO.criar(
            nome=nome,
            especialidade=especialidade,
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
@profissionais_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_profissional(id):
    try:
        # 1. Obtém o usuário logado
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        # 2. Verifica permissão
        # Admin pode atualizar qualquer profissional; profissional só pode atualizar a si mesmo
        if usuario['tipo'] == 'admin':
            pass  # autorizado
        elif usuario['tipo'] == 'profissional' and usuario.get('profissional_id') == id:
            pass  # autorizado
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        # 3. Valida o corpo da requisição
        data = request.get_json()
        if not data:
            return jsonify({'erro': 'Nenhum dado enviado para atualização'}), 400

        # (Opcional) Verifica se há pelo menos um campo válido
        campos_permitidos = ['nome', 'profissao', 'email', 'telefone', 'intervalo_minutos', 'ativo']
        if not any(campo in data for campo in campos_permitidos):
            return jsonify({'erro': 'Nenhum campo válido para atualização'}), 400

        # 4. Tenta atualizar no banco
        sucesso = ProfissionalDAO.atualizar(id, data)

        if not sucesso:
            # Pode ser que o profissional não exista ou nenhum campo foi alterado
            return jsonify({'erro': 'Profissional não encontrado ou nenhuma alteração realizada'}), 404

        return jsonify({'mensagem': 'Profissional atualizado com sucesso'}), 200

    except Exception as e:
        # 5. Tratamento de exceções inesperadas
        return jsonify({'erro': 'Erro interno no servidor'}), 500


# ------------------------------------------------------------
# Rota: DELETE /profissionais/<int:id>
# Descrição: Remove (fisicamente) um profissional
# ATENÇÃO: Isso apaga o registro do banco. Se quiser apenas desativar,
#          use a atualização com {"ativo": false}
# ------------------------------------------------------------
@profissionais_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@admin_required
def deletar_profissional(id):
    try:
        sucesso = ProfissionalDAO.deletar(id)
    except Exception as e:
        return jsonify({"erro": f"Erro ao deletar profissional: {str(e)}"}), 500

    if not sucesso:
        return jsonify({"erro": "Profissional não encontrado"}), 404

    return jsonify({"mensagem": "Profissional deletado com sucesso"}), 200


@profissionais_bp.route('/<int:id>/bloqueios', methods=['GET'])
@jwt_required()
def get_profissional_blocks(id):
    """
    Retorna todos os bloqueios de um profissional: dias, horários e recorrentes.
    Acesso permitido apenas para o próprio profissional ou admin.
    """
    try:
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        # Verifica permissão: admin ou próprio profissional
        if usuario['tipo'] != 'admin' and usuario.get('profissional_id') != id:
            return jsonify({'erro': 'Acesso negado'}), 403

        # Busca dias bloqueados
        dias = BloqueioDAO.dias_bloqueados(id)
        # Busca horários bloqueados
        horarios = BloqueioDAO.horarios_bloqueados_do_dia(id)  # retorna todos, sem filtrar data
        # Busca bloqueios recorrentes (sem filtro de data)
        recorrentes = BloqueioDAO.listar_bloqueios_recorrentes(profissional_id=id)

        # Converte datas para string ISO onde necessário
        for d in dias:
            if isinstance(d.get('data'), (date, datetime)):
                d['data'] = d['data'].isoformat()
        for h in horarios:
            if isinstance(h.get('data'), (date, datetime)):
                h['data'] = h['data'].isoformat()
        # Recorrentes já são convertidos pelo DAO

        return jsonify({
            'dias': dias,
            'horarios': horarios,
            'recorrentes': recorrentes
        }), 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao buscar bloqueios: {str(e)}'}), 500
