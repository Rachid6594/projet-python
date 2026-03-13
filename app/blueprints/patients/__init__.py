"""
Blueprint Patients
==================
Gestion du dossier patient : liste, création, modification, suppression.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime

from app.extensions import db
from app.utils.decorators import role_required
from app.models.patient import Patient

patients_bp = Blueprint('patients', __name__)


# ---------------------------------------------------------------------------
# Liste des patients
# ---------------------------------------------------------------------------

@patients_bp.route('/')
@login_required
@role_required('secretaire', 'admin')
def index():

    patients = Patient.query.order_by(Patient.nom).all()

    return render_template(
        'patients/index.html',
        patients=patients
    )


# ---------------------------------------------------------------------------
# Création patient
# ---------------------------------------------------------------------------

@patients_bp.route('/nouveau', methods=['GET', 'POST'])
@login_required
@role_required('secretaire', 'admin')
def create():

    if request.method == "POST":

        patient = Patient(
            nom=request.form["nom"],
            prenom=request.form["prenom"],
            date_naissance=datetime.strptime(
                request.form["date_naissance"], "%Y-%m-%d"
            ),
            telephone=request.form["telephone"],
            adresse=request.form["adresse"],
            sexe=request.form["sexe"]
        )

        db.session.add(patient)
        db.session.commit()

        flash("Patient ajouté avec succès", "success")

        return redirect(url_for("patients.index"))

    return render_template("patients/create.html")

# ---------------------------------------------------------------------------
# Modifier patient
# ---------------------------------------------------------------------------

@patients_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('secretaire', 'admin')
def edit(id):

    patient = Patient.query.get_or_404(id)

    if request.method == "POST":

        patient.nom = request.form["nom"]
        patient.prenom = request.form["prenom"]

        patient.date_naissance = datetime.strptime(
            request.form["date_naissance"], "%Y-%m-%d"
        )

        patient.telephone = request.form["telephone"]
        patient.adresse = request.form["adresse"]
        patient.sexe = request.form["sexe"]

        db.session.commit()

        flash("Patient modifié avec succès", "success")

        return redirect(url_for("patients.index"))

    return render_template(
        "patients/edit.html",
        patient=patient
    )

# ---------------------------------------------------------------------------
# Supprimer patient
# ---------------------------------------------------------------------------

@patients_bp.route('/<int:id>/supprimer', methods=['POST'])
@login_required
@role_required('secretaire', 'admin')
def delete(id):

    patient = Patient.query.get_or_404(id)

    db.session.delete(patient)
    db.session.commit()

    flash("Patient supprimé avec succès", "info")

    return redirect(url_for("patients.index"))

# ---------------------------------------------------------------------------
# Historique médical du patient
# ---------------------------------------------------------------------------

from datetime import date
from app.models.rendez_vous import RendezVous
from app.models.consultation import Consultation

@patients_bp.route('/<int:id>')
@login_required
@role_required('secretaire', 'admin')
def show(id):

    patient = Patient.query.get_or_404(id)

    # RDV à venir
    rdv_a_venir = (
        RendezVous.query
        .filter(RendezVous.patient_id == id, RendezVous.date >= date.today())
        .order_by(RendezVous.date.asc())
        .all()
    )

    # Consultations passées (via le RDV)
    consultations = (
        Consultation.query
        .join(RendezVous, Consultation.rendez_vous_id == RendezVous.id)
        .filter(RendezVous.patient_id == id)
        .order_by(Consultation.id.desc())
        .all()
    )

    return render_template(
        "patients/show.html",
        patient=patient,
        rdv_a_venir=rdv_a_venir,
        consultations=consultations
    )