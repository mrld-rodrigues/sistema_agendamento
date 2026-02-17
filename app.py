from flask import Flask
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


app.register_blueprint(clientes_bp, url_prefix="/clientes")
app.register_blueprint(profissionais_bp, url_prefix="/profissionais")
app.register_blueprint(servicos_bp, url_prefix="/servicos")
app.register_blueprint(agendamentos_bp, url_prefix="/agendamentos")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(bloqueios_bp, url_prefix="/bloqueios")
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
