from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from dao.user_dao import UsuarioDAO

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario or usuario['tipo'] != 'admin':
            return jsonify({'erro': 'Acesso negado'}), 403
        return fn(*args, **kwargs)
    return wrapper

def profissional_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario or usuario['tipo'] not in ['admin', 'profissional']:
            return jsonify({'erro': 'Acesso negado'}), 403
        return fn(*args, **kwargs)
    return wrapper

def cliente_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        usuario = UsuarioDAO.buscar_por_id(user_id)
        if not usuario or usuario['tipo'] not in ['admin', 'cliente']:
            return jsonify({'erro': 'Acesso negado'}), 403
        return fn(*args, **kwargs)
    return wrapper