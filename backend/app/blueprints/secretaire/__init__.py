"""
Blueprint Secrétaire
====================
Point d'entrée de l'espace secrétaire.

Membre 1 (nous) : uniquement la route d'accueil + protection par rôle.
Membres 2 & 3   : ajoutent leurs routes dans ce blueprint ou dans
                  les blueprints patients / medecins / rendez_vous.

Templates : frontend/templates/secretaire/
"""

from flask import Blueprint, render_template
from flask_login import login_required

from app.utils.decorators import role_required

secretaire_bp = Blueprint('secretaire', __name__)


@secretaire_bp.route('/')
@login_required
@role_required('secretaire', 'admin')
def index():
    """Page d'accueil de l'espace secrétaire."""
    return render_template('secretaire/index.html')
