import os
from flask import Flask, redirect, url_for
from flask_login import current_user
from app.extensions import db, login_manager, bcrypt, migrate
from config import config


def create_app(config_name='default'):
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

    app = Flask(
        __name__,
        template_folder=FRONTEND_DIR,
        static_folder=os.path.join(FRONTEND_DIR, 'assets'),
        static_url_path='/static'
    )
    app.config.from_object(config[config_name])

    # CSRF (Flask-WTF) pour que csrf_token soit disponible dans les templates
    from flask_wtf.csrf import CSRFProtect
    CSRFProtect(app)

    # Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    from app.routes.auth import auth
    from app.routes.secretaire import secretaire
    from app.routes.medecin import medecin_bp

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(secretaire, url_prefix='/secretaire')
    app.register_blueprint(medecin_bp, url_prefix='/medecin')

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.role == 'secretaire':
                return redirect(url_for('secretaire.dashboard'))
            return redirect(url_for('medecin.dashboard'))
        return redirect(url_for('auth.login'))

    return app
