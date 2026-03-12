"""
Blueprint Patients
==================
Gestion du dossier patient : liste, création, modification, suppression.

Accès réservé aux rôles : 'secretaire', 'admin'.

Routes prévues (à implémenter) :
  GET     /patients/          → liste des patients
  GET/POST /patients/nouveau  → créer un patient
  GET     /patients/<id>      → fiche détaillée
  GET/POST /patients/<id>/edit → modifier un patient
  POST    /patients/<id>/supprimer → supprimer un patient
"""

from flask import Blueprint, render_template
from flask_login import login_required

from app.utils.decorators import role_required

patients_bp = Blueprint('patients', __name__)


# ---------------------------------------------------------------------------
# Liste des patients — dashboard secrétaire
# ---------------------------------------------------------------------------

@patients_bp.route('/')
@login_required
@role_required('secretaire', 'admin')
def index():
    """Affiche la liste de tous les patients."""
    # TODO : pagination, recherche
    from app.models.patient import Patient
    patients = Patient.query.order_by(Patient.nom).all()
    return render_template('patients/index.html', patients=patients)
