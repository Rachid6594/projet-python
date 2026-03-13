"""
Blueprint Médecin (espace personnel)
=====================================
Point d'entrée de l'espace médecin connecté.

Membre 1 (nous) : uniquement la route d'accueil + protection par rôle.
Membre 4        : ajoute le calendrier, les consultations, le tableau de bord
                  dans ce blueprint.

À ne pas confondre avec le blueprint 'medecins' (annuaire des médecins,
géré par Membre 3).

Templates : frontend/templates/medecin/
"""

from flask import Blueprint, render_template
from flask_login import login_required

from app.utils.decorators import role_required

medecin_bp = Blueprint('medecin', __name__)


@medecin_bp.route('/')
@login_required
@role_required('medecin')
def index():
    """Page d'accueil de l'espace médecin connecté."""
    return render_template('medecin/index.html')
