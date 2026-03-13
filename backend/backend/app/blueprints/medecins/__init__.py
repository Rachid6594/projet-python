"""
Blueprint Médecins
==================
Gestion des fiches médecins : liste et détail.

Accès réservé aux rôles : 'secretaire', 'admin'.

Routes prévues (à implémenter) :
  GET      /medecins/          → liste des médecins
  GET/POST /medecins/nouveau   → créer une fiche médecin (+ compte utilisateur)
  GET      /medecins/<id>      → détail d'un médecin
  GET/POST /medecins/<id>/edit → modifier la fiche
"""

from flask import Blueprint, render_template
from flask_login import login_required

from app.utils.decorators import role_required

medecins_bp = Blueprint('medecins', __name__)


# ---------------------------------------------------------------------------
# Liste des médecins
# ---------------------------------------------------------------------------

@medecins_bp.route('/')
@login_required
@role_required('secretaire', 'admin')
def index():
    """Affiche la liste de tous les médecins du cabinet."""
    # TODO : filtrage par spécialité
    from app.models.medecin import Medecin
    medecins = Medecin.query.order_by(Medecin.nom).all()
    return render_template('medecins/index.html', medecins=medecins)
