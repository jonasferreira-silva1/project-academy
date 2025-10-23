from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_wtf import CSRFProtect
import os
from flask_wtf.csrf import generate_csrf
from domain import db
from services import load_user
from services.rate_limit_service import usuarios_bloqueados

from routes import register_blueprints

load_dotenv()

app = Flask(__name__,
            template_folder='/app/templates',
            static_folder='/app/static')

app.secret_key = os.getenv('FLASK_SECRET_KEY')
if not app.secret_key:
    raise RuntimeError(
        "A variável FLASK_SECRET_KEY não está definida no ambiente!")

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError(
        "A variável DATABASE_URL não está definida no ambiente!")


if database_url.startswith("mysql://"):
    database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)


app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Atualizado para usar blueprint


csrf = CSRFProtect(app)


# Comentado temporariamente para evitar erro de conexão
with app.app_context():
    db.create_all()  # Cria tabelas do banco
    print("Tabelas criadas com sucesso!")


@login_manager.user_loader
def load_user_wrapper(user_id):
    """Carrega usuário para Flask-Login."""
    return load_user(user_id)


register_blueprints(app)


# Configuração CSRF e cookies (controlado por variável de ambiente para segurança)
use_https = os.getenv('USE_HTTPS', 'False').lower() == 'true'
app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=use_https  # Controlado por USE_HTTPS
)


@app.context_processor
def inject_csrf_token():
    """Injeta token CSRF nos templates."""
    return dict(csrf_token=generate_csrf)


@app.after_request
def set_csrf_cookie(response):
    """Define cookie CSRF."""
    try:
        csrf_token_value = generate_csrf()
        response.set_cookie(
            "csrf_token",
            csrf_token_value,
            secure=use_https,  # Controlado por USE_HTTPS
            samesite="Lax",
            path="/"
        )
    except Exception:
        pass
    return response


if __name__ == "__main__":
    # Host para acesso externo
    # Debug mode controlado por variável de ambiente para segurança
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0')
