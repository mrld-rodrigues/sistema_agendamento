from flask import Flask, jsonify, render_template, request
from dao.client_dao import ClienteDAO
from dao.professional_dao import ProfissionalDAO
from dao.service_dao import ServicoDAO
from routes.clients_routes import clientes_bp
from routes.professionals_routes import profissionais_bp
from routes.services_routes import servicos_bp
from routes.scheduling_routes import agendamentos_bp
from routes.admin_routes import admin_bp
from routes.blocked_routes import bloqueios_bp
from flask_jwt_extended import JWTManager, jwt_required
from routes.auth_routes import auth_bp
import os

from utils.decorators import admin_required


app = Flask(__name__)
app.json.ensure_ascii = False  # Permitir caracteres Unicode no JSON

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')  
jwt = JWTManager(app)

# Registro dos blueprints da API
app.register_blueprint(clientes_bp, url_prefix="/clientes")
app.register_blueprint(profissionais_bp, url_prefix="/profissionais")
app.register_blueprint(servicos_bp, url_prefix="/servicos")
app.register_blueprint(agendamentos_bp, url_prefix="/agendamentos")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(bloqueios_bp, url_prefix="/bloqueios")
app.register_blueprint(auth_bp, url_prefix='/auth')


# ---------- Rotas para páginas frontend (HTML) ----------
# Páginas públicas
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auth/login')
def login_page():
    return render_template('auth/login.html')

@app.route('/auth/register')
def register_page():
    return render_template('auth/register.html')

# Páginas do cliente (protegidas por autenticação no frontend)
@app.route('/client/dashboard')
def client_dashboard():
    return render_template('client/dashboard.html')

@app.route('/client/new-appointment')
def client_new_appointment():
    return render_template('client/new_appointment.html')


# Páginas do profissional (protegidas por autenticação no frontend)
@app.route('/professional/dashboard')
def professional_dashboard():
    return render_template('professional/dashboard.html')

@app.route('/professional/settings')
def professional_settings():
    return render_template('professional/settings.html')

@app.route('/professional/blocks')
def professional_blocks():
    return render_template('professional/blocked_days.html')



# Páginas do admin (protegidas por autenticação no frontend)
@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')

@app.route('/admin/clients')
def admin_clients():
    return render_template('admin/clients.html')

@app.route('/admin/clients/new')
def admin_client_new():
    return render_template('admin/client_form.html')  # criaremos depois

@app.route('/admin/clients/<int:id>/edit')
def admin_client_edit(id):
    return render_template('admin/client_form.html', client_id=id)


# -------------------- CLIENTES (Admin) --------------------
@admin_bp.route('/clients', methods=['GET'])
@jwt_required()
@admin_required
def listar_clientes_admin():
    """Retorna a lista de todos os clientes (para admin)."""
    try:
        clientes = ClienteDAO.listar()
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# -------------------- PROFISSIONAIS (Admin) --------------------
@admin_bp.route('/professionals', methods=['GET'])
@jwt_required()
@admin_required
def listar_profissionais_admin():
    """Retorna a lista de todos os profissionais (para admin)."""
    try:
        # Por padrão, listar apenas ativos? Admin pode querer ver todos.
        # Vamos permitir passar um parâmetro para incluir inativos.
        incluir_inativos = request.args.get('incluir_inativos', 'false').lower() == 'true'
        apenas_ativos = not incluir_inativos
        profissionais = ProfissionalDAO.listar(apenas_ativos=apenas_ativos)
        return jsonify(profissionais), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# -------------------- SERVIÇOS (Admin) --------------------
@admin_bp.route('/services', methods=['GET'])
@jwt_required()
@admin_required
def listar_servicos_admin():
    """Retorna a lista de todos os serviços (para admin)."""
    try:
        incluir_inativos = request.args.get('incluir_inativos', 'false').lower() == 'true'
        apenas_ativos = not incluir_inativos
        servicos = ServicoDAO.listar(apenas_ativos=apenas_ativos)
        return jsonify(servicos), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
