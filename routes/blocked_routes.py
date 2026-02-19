from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from dao.blocked_dao import BloqueioDAO
from dao.user_dao import UsuarioDAO



bloqueios_bp = Blueprint("bloqueios", __name__)


# -------------------- BLOQUEAR DIA --------------------
@bloqueios_bp.route('/bloquear-dia', methods=['POST'])
@jwt_required()
def bloquear_dia():
    try:
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        data = request.get_json()
        if not data or 'profissional_id' not in data or 'data' not in data:
            return jsonify({'erro': 'Campos obrigatórios: profissional_id, data'}), 400

        profissional_id = data['profissional_id']

        # Verifica permissão
        if usuario['tipo'] == 'admin':
            pass
        elif usuario['tipo'] == 'profissional' and profissional_id == usuario.get('profissional_id'):
            pass
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        BloqueioDAO.bloquear_dia(profissional_id, data['data'], data.get('motivo'))
        return jsonify({'mensagem': 'Dia bloqueado com sucesso'}), 201
    except Exception as e:
        print(f"Erro em POST /bloqueios/bloquear-dia: {str(e)}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500


# -------------------- BLOQUEAR HORÁRIO --------------------
@bloqueios_bp.route('/bloquear-horario', methods=['POST'])
@jwt_required()
def bloquear_horario():
    try:
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        data = request.get_json()
        campos = ['profissional_id', 'data', 'hora_inicio', 'hora_fim']
        if not all(c in data for c in campos):
            return jsonify({"erro": f"Campos obrigatórios: {', '.join(campos)}"}), 400

        profissional_id = data['profissional_id']

        # Verifica permissão
        if usuario['tipo'] == 'admin':
            pass
        elif usuario['tipo'] == 'profissional' and profissional_id == usuario.get('profissional_id'):
            pass
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        BloqueioDAO.bloquear_horario(
            profissional_id,
            data['data'],
            data['hora_inicio'],
            data['hora_fim'],
            data.get('motivo')
        )
        return jsonify({'mensagem': 'Horário bloqueado com sucesso'}), 201
    except Exception as e:
        print(f"Erro em POST /bloqueios/bloquear-horario: {str(e)}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500


# -------------------- BLOQUEAR PERÍODO --------------------
@bloqueios_bp.route('/bloquear-periodo', methods=['POST'])
@jwt_required()
def bloquear_periodo():
    try:
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        data = request.get_json()
        campos = ['profissional_id', 'data_inicio', 'data_fim']
        if not all(c in data for c in campos):
            return jsonify({"erro": f"Campos obrigatórios: {', '.join(campos)}"}), 400

        profissional_id = data['profissional_id']

        # Verifica permissão
        if usuario['tipo'] == 'admin':
            pass
        elif usuario['tipo'] == 'profissional' and profissional_id == usuario.get('profissional_id'):
            pass
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        BloqueioDAO.bloquear_periodo(
            profissional_id,
            data['data_inicio'],
            data['data_fim'],
            data.get('motivo')
        )
        return jsonify({'mensagem': 'Período bloqueado com sucesso'}), 201
    except Exception as e:
        print(f"Erro em POST /bloqueios/bloquear-periodo: {str(e)}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500


# -------------------- LISTAR TODOS (admin vê todos, profissional vê próprios) --------------------
@bloqueios_bp.route('/todos', methods=['GET'])
@jwt_required()
def listar_todos_bloqueios():
    try:
        profissional_id = request.args.get('profissional_id', type=int)
        data = request.args.get('data')
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        if usuario['tipo'] == 'admin':
            if not profissional_id:
                return jsonify({'erro': 'Informe profissional_id'}), 400
            dados = BloqueioDAO.listar_todos_bloqueios(profissional_id, data)
        elif usuario['tipo'] == 'profissional':
            dados = BloqueioDAO.listar_todos_bloqueios(usuario['profissional_id'], data)
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        return jsonify(dados), 200
    except Exception as e:
        print(f"Erro em GET /bloqueios/todos: {str(e)}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500


# -------------------- DIAS BLOQUEADOS --------------------
@bloqueios_bp.route('/dias-bloqueados', methods=['GET'])
@jwt_required()
def dias_bloqueados():
    try:
        profissional_id = request.args.get('profissional_id', type=int)
        data = request.args.get('data')
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        # Permissão: admin pode ver qualquer, profissional só os seus
        if usuario['tipo'] == 'admin':
            if not profissional_id:
                return jsonify({'erro': 'Informe profissional_id'}), 400
            dados = BloqueioDAO.dias_bloqueados(profissional_id, data)
        elif usuario['tipo'] == 'profissional':
            dados = BloqueioDAO.dias_bloqueados(usuario['profissional_id'], data)
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        return jsonify(dados), 200
    except Exception as e:
        print(f"Erro em GET /bloqueios/dias-bloqueados: {str(e)}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500


# -------------------- HORÁRIOS BLOQUEADOS --------------------
@bloqueios_bp.route('/horarios-bloqueados', methods=['GET'])
@jwt_required()
def horarios_bloqueados():
    try:
        profissional_id = request.args.get('profissional_id', type=int)
        data = request.args.get('data')
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        if usuario['tipo'] == 'admin':
            if not profissional_id:
                return jsonify({'erro': 'Informe profissional_id'}), 400
            dados = BloqueioDAO.horarios_bloqueados_do_dia(profissional_id, data)
        elif usuario['tipo'] == 'profissional':
            dados = BloqueioDAO.horarios_bloqueados_do_dia(usuario['profissional_id'], data)
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        return jsonify(dados), 200
    except Exception as e:
        print(f"Erro em GET /bloqueios/horarios-bloqueados: {str(e)}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500


# -------------------- APAGAR DIA --------------------
@bloqueios_bp.route('/apagar-dia/<int:bloqueio_id>', methods=['DELETE'])
@jwt_required()
def apagar_bloqueios_dia(bloqueio_id):
    try:
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        # Buscar o bloqueio para verificar propriedade
        # Nota: você precisa implementar BloqueioDAO.buscar_bloqueio_dia_por_id(bloqueio_id)
        # Se não tiver, podemos pular a verificação e deixar que o profissional só possa deletar se for dele?
        # Por segurança, vamos adicionar uma verificação após buscar.
        # Por enquanto, vou assumir que o método existe.
        bloqueio = BloqueioDAO.buscar_bloqueio_dia_por_id(bloqueio_id)
        if not bloqueio:
            return jsonify({'erro': 'Bloqueio não encontrado'}), 404

        if usuario['tipo'] != 'admin' and bloqueio['profissional_id'] != usuario.get('profissional_id'):
            return jsonify({'erro': 'Acesso negado'}), 403

        sucesso = BloqueioDAO.apagar_bloqueios_dia(bloqueio_id)
        if not sucesso:
            return jsonify({'erro': 'Bloqueio não encontrado'}), 404

        return jsonify({'mensagem': 'Bloqueio removido'}), 200
    except Exception as e:
        print(f"Erro em DELETE /bloqueios/apagar-dia/{bloqueio_id}: {str(e)}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500


# -------------------- APAGAR HORÁRIO --------------------
@bloqueios_bp.route('/apagar-horario/<int:bloqueio_id>', methods=['DELETE'])
@jwt_required()
def apagar_bloqueios_horario(bloqueio_id):
    try:
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        # Buscar bloqueio de horário
        bloqueio = BloqueioDAO.buscar_bloqueio_horario_por_id(bloqueio_id)
        if not bloqueio:
            return jsonify({'erro': 'Bloqueio não encontrado'}), 404

        if usuario['tipo'] != 'admin' and bloqueio['profissional_id'] != usuario.get('profissional_id'):
            return jsonify({'erro': 'Acesso negado'}), 403

        sucesso = BloqueioDAO.apagar_bloqueios_horario(bloqueio_id)
        if not sucesso:
            return jsonify({'erro': 'Bloqueio não encontrado'}), 404

        return jsonify({'mensagem': 'Bloqueio removido'}), 200
    except Exception as e:
        print(f"Erro em DELETE /bloqueios/apagar-horario/{bloqueio_id}: {str(e)}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500


# -------------------- CRIAR BLOQUEIO RECORRENTE --------------------
@bloqueios_bp.route('/recorrente', methods=['POST'])
@jwt_required()
def criar_bloqueio_recorrente():
    try:
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        data = request.get_json()
        campos = ['profissional_id', 'dia_semana', 'hora_inicio', 'hora_fim']
        if not all(c in data for c in campos):
            return jsonify({"erro": f"Campos obrigatórios: {', '.join(campos)}"}), 400

        profissional_id = data['profissional_id']

        if usuario['tipo'] == 'admin':
            pass
        elif usuario['tipo'] == 'profissional' and profissional_id == usuario.get('profissional_id'):
            pass
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        bloqueio_id = BloqueioDAO.criar_bloqueio_recorrente(
            profissional_id=profissional_id,
            dia_semana=data['dia_semana'],
            hora_inicio=data['hora_inicio'],
            hora_fim=data['hora_fim'],
            data_inicio=data.get('data_inicio'),
            data_fim=data.get('data_fim'),
            motivo=data.get('motivo')
        )
        return jsonify({'id': bloqueio_id, 'mensagem': 'Bloqueio recorrente criado com sucesso'}), 201
    except Exception as e:
        print(f"Erro em POST /bloqueios/recorrente: {str(e)}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500


# -------------------- LISTAR BLOQUEIOS RECORRENTES --------------------
@bloqueios_bp.route('/recorrentes', methods=['GET'])
@jwt_required()
def listar_bloqueios_recorrentes():
    try:
        profissional_id = request.args.get('profissional_id', type=int)
        data_ref = request.args.get('data')
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        if usuario['tipo'] == 'admin':
            # admin pode ver de qualquer profissional
            if not profissional_id:
                return jsonify({'erro': 'Informe profissional_id'}), 400
            bloqueios = BloqueioDAO.listar_bloqueios_recorrentes(profissional_id, data_ref)
        elif usuario['tipo'] == 'profissional':
            bloqueios = BloqueioDAO.listar_bloqueios_recorrentes(usuario['profissional_id'], data_ref)
        else:
            return jsonify({'erro': 'Acesso negado'}), 403

        return jsonify(bloqueios), 200
    except Exception as e:
        print(f"Erro em GET /bloqueios/recorrentes: {str(e)}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500


# -------------------- DELETAR BLOQUEIO RECORRENTE --------------------
@bloqueios_bp.route('/recorrente/<int:bloqueio_id>', methods=['DELETE'])
@jwt_required()
def deletar_bloqueio_recorrente(bloqueio_id):
    try:
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        # Buscar bloqueio recorrente
        bloqueio = BloqueioDAO.buscar_bloqueio_recorrente_por_id(bloqueio_id)
        if not bloqueio:
            return jsonify({'erro': 'Bloqueio recorrente não encontrado'}), 404

        if usuario['tipo'] != 'admin' and bloqueio['profissional_id'] != usuario.get('profissional_id'):
            return jsonify({'erro': 'Acesso negado'}), 403

        sucesso = BloqueioDAO.apagar_bloqueio_recorrente(bloqueio_id)
        if not sucesso:
            return jsonify({'erro': 'Bloqueio recorrente não encontrado'}), 404

        return jsonify({'mensagem': 'Bloqueio recorrente removido com sucesso'}), 200
    except Exception as e:
        print(f"Erro em DELETE /bloqueios/recorrente/{bloqueio_id}: {str(e)}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500