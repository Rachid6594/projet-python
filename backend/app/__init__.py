import os
from datetime import datetime, timezone
from flask import Flask, redirect, url_for
from flask_login import current_user
from jinja2 import ChoiceLoader, FileSystemLoader

from app.extensions import db, login_manager, migrate
from config import config


def create_app(config_name='default'):
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    _ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    _FRONTEND_TEMPLATES  = os.path.join(_ROOT, 'frontend', 'templates')
    _FRONTEND_COMPONENTS = os.path.join(_ROOT, 'frontend', 'components')

    app = Flask(__name__, template_folder=_FRONTEND_TEMPLATES)
    app.config.from_object(config[config_name])

    # Loader Jinja2 : templates/ puis components/
    app.jinja_loader = ChoiceLoader([
        FileSystemLoader(_FRONTEND_TEMPLATES),
        FileSystemLoader(_FRONTEND_COMPONENTS),
    ])

    # Extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Modeles (pour Alembic)
    from app import models as _models  # noqa: F401

    # Blueprints
    from app.blueprints.auth       import auth_bp
    from app.blueprints.admin      import admin_bp
    from app.blueprints.secretaire import secretaire_bp
    from app.blueprints.patients   import patients_bp
    from app.blueprints.medecins   import medecins_bp
    from app.blueprints.rendez_vous import rendez_vous_bp
    from app.blueprints.medecin       import medecin_bp
    from app.blueprints.consultations import consultations_bp
    from app.blueprints.ordonnances   import ordonnances_bp
    from app.blueprints.statistiques  import statistiques_bp

    app.register_blueprint(auth_bp,          url_prefix='/auth')
    app.register_blueprint(admin_bp,         url_prefix='/admin')
    app.register_blueprint(secretaire_bp,    url_prefix='/secretaire')
    app.register_blueprint(patients_bp,      url_prefix='/patients')
    app.register_blueprint(medecins_bp,      url_prefix='/medecins')
    app.register_blueprint(rendez_vous_bp,   url_prefix='/rendez-vous')
    app.register_blueprint(medecin_bp,       url_prefix='/medecin')
    app.register_blueprint(consultations_bp, url_prefix='/consultations')
    app.register_blueprint(ordonnances_bp,   url_prefix='/ordonnances')
    app.register_blueprint(statistiques_bp,  url_prefix='/statistiques')

    # Context processor
    @app.context_processor
    def inject_globals():
        return {'current_year': datetime.now(timezone.utc).year}

    # Route racine
    @app.route('/')
    def index():
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.role == 'admin':
            return redirect(url_for('admin.index'))
        if current_user.role == 'medecin':
            return redirect(url_for('medecin.index'))
        return redirect(url_for('secretaire.index'))

    return app
