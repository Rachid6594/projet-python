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
from sqlalchemy import extract
from datetime import datetime

from app.models.patient import Patient
from app.models.medecin import Medecin
from app.models.rendez_vous import RendezVous
from app.models.consultation import Consultation

secretaire_bp = Blueprint('secretaire', __name__)

@secretaire_bp.route('/')
@login_required
@role_required('secretaire', 'admin')
def index():

    total_patients = Patient.query.count()
    total_medecins = Medecin.query.count()
    total_rdv = RendezVous.query.count()

    # Mois du graphique
    months = [
        "J","F","M","A","M","J",
        "J","A","S","O","N","D"
    ]

    current_year = datetime.now().year

    # Consultations par mois
    consultations_data = []

    for m in range(1,13):

        count = Consultation.query.filter(
            extract('month', Consultation.date_creation) == m,
            extract('year', Consultation.date_creation) == current_year
        ).count()

        consultations_data.append(count)

    return render_template(
        'secretaire/index.html',
        total_patients=total_patients,
        total_medecins=total_medecins,
        total_rdv=total_rdv,
        months=months,
        consultations_data=consultations_data
    )

    total_patients = Patient.query.count()
    total_medecins = Medecin.query.count()
    total_rdv = RendezVous.query.count()

    return render_template(
        'secretaire/index.html',
        total_patients=total_patients,
        total_medecins=total_medecins,
        total_rdv=total_rdv
    )