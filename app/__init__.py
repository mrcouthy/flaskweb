from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    login.login_view = 'auth.login'  # Tell Flask-Login where the login route is
    login.login_message_category = 'info' # Category for the "Please log in" message

    # Register blueprints here
    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
