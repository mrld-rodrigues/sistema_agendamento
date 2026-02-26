from flask import Flask, render_template
from routes.clients_routes import clientes_bp
from routes.professionals_routes import profissionais_bp
from routes.services_routes import servicos_bp
from routes.scheduling_routes import agendamentos_bp
from routes.admin_routes import admin_bp
from routes.blocked_routes import bloqueios_bp
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_bp
import os


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
@app.route('/')
def index():
    """Página inicial pública."""
    return render_template('index.html')

@app.route('/auth/login')
def auth_login():
    """Página de login."""
    return render_template('auth/login.html')

@app.route('/auth/registro/cliente')
def auth_registro_cliente():
    """Página de registro de cliente."""
    return render_template('auth/registro_cliente.html')

@app.route('/cliente/dashboard')
def cliente_dashboard():
    """Dashboard do cliente (requer autenticação no frontend)."""
    return render_template('cliente/dashboard.html')

@app.route('/cliente/novo-agendamento')
def cliente_novo_agendamento():
    """Página para criar novo agendamento (cliente)."""
    return render_template('cliente/novo_agendamento.html')



if __name__ == "__main__":
    app.run(debug=True, threaded=True)
