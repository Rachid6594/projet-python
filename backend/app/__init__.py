"""
Factory de l'application Flask
================================
Crée et configure l'instance Flask via le pattern Application Factory.
Cela permet d'instancier l'app avec différentes configurations (dev, prod, test)
et facilite les tests unitaires.

Redirections après connexion (gérées par Membre 1) :
  - admin      → /admin/
  - secretaire → /secretaire/   (espace Membres 2 & 3)
  - medecin    → /medecin/      (espace Membre 4)
"""

import os
from datetime import datetime, timezone

from flask import Flask, redirect, url_for
from flask_login import current_user
from jinja2 import ChoiceLoader, FileSystemLoader

from app.extensions import db, login_manager, migrate
from config import config

# ── Chemins absolus vers les dossiers frontend ──────────────────────────────
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_FRONTEND_TEMPLATES  = os.path.join(_ROOT, 'frontend', 'templates')
_FRONTEND_COMPONENTS = os.path.join(_ROOT, 'frontend', 'components')


def create_app(config_name: str = 'default') -> Flask:
    flask_app = Flask(__name__, template_folder=_FRONTEND_TEMPLATES)
    flask_app.config.from_object(config[config_name])

    # ── Loader Jinja2 : templates/ puis components/ ───────────────────────
    flask_app.jinja_loader = ChoiceLoader([
        FileSystemLoader(_FRONTEND_TEMPLATES),
        FileSystemLoader(_FRONTEND_COMPONENTS),
    ])

    # ── Extensions ────────────────────────────────────────────────────────
    db.init_app(flask_app)
    login_manager.init_app(flask_app)
    migrate.init_app(flask_app, db)

    # ── Modèles (side-effect pour Alembic) ────────────────────────────────
    from app import models as _models  # noqa: F401

    # ── Blueprints ────────────────────────────────────────────────────────
    # Membre 1 — auth & admin
    from app.blueprints.auth       import auth_bp
    from app.blueprints.admin      import admin_bp

    # Espace secrétaire (Membres 2 & 3 ajoutent leurs routes ici)
    from app.blueprints.secretaire import secretaire_bp
    from app.blueprints.patients   import patients_bp        # Membre 2
    from app.blueprints.medecins   import medecins_bp        # Membre 3
    from app.blueprints.rendez_vous import rendez_vous_bp    # Membre 3

    # Espace médecin (Membre 4 ajoute ses routes ici)
    from app.blueprints.medecin       import medecin_bp
    from app.blueprints.consultations import consultations_bp  # Membre 4

    flask_app.register_blueprint(auth_bp,          url_prefix='/auth')
    flask_app.register_blueprint(admin_bp,         url_prefix='/admin')
    flask_app.register_blueprint(secretaire_bp,    url_prefix='/secretaire')
    flask_app.register_blueprint(patients_bp,      url_prefix='/patients')
    flask_app.register_blueprint(medecins_bp,      url_prefix='/medecins')
    flask_app.register_blueprint(rendez_vous_bp,   url_prefix='/rendez-vous')
    flask_app.register_blueprint(medecin_bp,       url_prefix='/medecin')
    flask_app.register_blueprint(consultations_bp, url_prefix='/consultations')

    # ── Context processor ─────────────────────────────────────────────────
    @flask_app.context_processor
    def inject_globals() -> dict:
        return {'current_year': datetime.now(timezone.utc).year}

    # ── Route racine — redirections selon le rôle (Membre 1) ─────────────
    @flask_app.route('/')
    def index():
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.role == 'admin':
            return redirect(url_for('admin.index'))
        if current_user.role == 'medecin':
            return redirect(url_for('medecin.index'))
        # secretaire (et tout autre rôle futur)
        return redirect(url_for('secretaire.index'))

    return flask_app
