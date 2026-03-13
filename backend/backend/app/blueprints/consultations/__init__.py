"""
Blueprint Consultations
=======================
Saisie et consultation des comptes-rendus médicaux.

- Médecins     : créer et modifier leurs propres consultations
- Secrétaires  : lecture seule (accès en consultation uniquement)

Routes prévues (à implémenter) :
  GET      /consultations/                 → liste des consultations
  GET/POST /consultations/rdv/<rdv_id>/new → créer la consultation d'un RDV
  GET      /consultations/<id>             → lire un compte-rendu
  GET/POST /consultations/<id>/edit        → modifier (médecin propriétaire)
"""

from flask import Blueprint, render_template
from flask_login import login_required

from app.utils.decorators import role_required

consultations_bp = Blueprint('consultations', __name__)


# ---------------------------------------------------------------------------
# Liste des consultations
# ---------------------------------------------------------------------------

@consultations_bp.route('/')
@login_required
@role_required('secretaire', 'admin', 'medecin')
def index():
    """Affiche la liste des consultations (toutes, ou filtrée par médecin)."""
    # TODO : filtre par médecin, par date
    from app.models.consultation import Consultation
    consultations = Consultation.query.order_by(
        Consultation.date_creation.desc()
    ).all()
    return render_template('consultations/index.html', consultations=consultations)
