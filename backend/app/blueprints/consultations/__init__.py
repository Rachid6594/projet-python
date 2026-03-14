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

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, date
from app.models.consultation import Consultation
from app.models.rendez_vous import RendezVous
from app.models.patient import Patient
from app.models.medecin import Medecin
from app import db

consultations_bp = Blueprint('consultations', __name__, url_prefix='/consultations')


# ---------------------------------------------------------------------------
# Liste des consultations
# ---------------------------------------------------------------------------

@consultations_bp.route('/')
@login_required
def index():
    """Affiche la liste des consultations (toutes, ou filtrée par médecin)."""
    # TODO : filtre par médecin, par date
    consultations = Consultation.query.order_by(
        Consultation.created_at.desc()
    ).all()
    return render_template('consultations/index.html', consultations=consultations)


# ---------------------------------------------------------------------------
# Création d'une consultation
# ---------------------------------------------------------------------------

@consultations_bp.route('/demarrer/<int:rdv_id>', methods=['GET', 'POST'])
@login_required
def demarrer(rdv_id):
    rdv = RendezVous.query.get_or_404(rdv_id)
    patient = Patient.query.get_or_404(rdv.patient_id)
    medecin = Medecin.query.filter_by(utilisateur_id=current_user.id).first()
    if not medecin or rdv.medecin_id != medecin.id:
        return "Accès interdit", 403

    # Historique des consultations du patient
    historique = Consultation.query \
        .join(RendezVous, Consultation.rendez_vous_id == RendezVous.id) \
        .filter(RendezVous.patient_id == patient.id) \
        .order_by(Consultation.created_at.desc()) \
        .all()

    if request.method == 'POST':
        symptomes = request.form.get('symptomes')
        diagnostic = request.form.get('diagnostic')
        traitement = request.form.get('traitement')
        observations = request.form.get('observations')

        # Création de la consultation
        consultation = Consultation(
            rendez_vous_id=rdv.id,
            symptomes=symptomes,
            diagnostic=diagnostic,
            traitement=traitement,
            observations=observations,
            created_at=datetime.utcnow()
        )
        db.session.add(consultation)
        # Passage du RDV au statut "effectué"
        rdv.statut = 'effectue'
        db.session.commit()
        flash("Consultation enregistrée avec succès.", "success")
        return redirect(url_for('medecin.calendrier'))

    # Calcul de l'âge du patient
    age = date.today().year - patient.date_naissance.year - (
        (date.today().month, date.today().day) < (patient.date_naissance.month, patient.date_naissance.day)
    )

    return render_template(
        'consultations/demarrer.html',
        patient=patient,
        age=age,
        rdv=rdv,
        historique=historique
    )
