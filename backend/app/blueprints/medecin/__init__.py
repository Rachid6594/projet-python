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
from flask_login import login_required, current_user
from datetime import date, datetime
from sqlalchemy import extract, func
from app.models.medecin import Medecin
from app.models.rendez_vous import RendezVous
from app.models.consultation import Consultation
from app.models.patient import Patient
from flask import jsonify

medecin_bp = Blueprint('medecin', __name__, url_prefix='/medecin')


@medecin_bp.route('/')
@login_required
def index():
    """Page d'accueil de l'espace médecin connecté."""
    # Récupérer le médecin connecté
    medecin = Medecin.query.filter_by(utilisateur_id=current_user.id).first()
    if not medecin:
        return "Aucun profil médecin associé.", 403

    # Rendez-vous du jour
    today = date.today()
    rdv_du_jour = RendezVous.query.filter_by(medecin_id=medecin.id, date=today).order_by(RendezVous.heure).all()

    # Statistiques personnelles
    mois = today.month
    annee = today.year
    consultations_mois = Consultation.query \
        .join(RendezVous, Consultation.rendez_vous_id == RendezVous.id) \
        .filter(RendezVous.medecin_id == medecin.id) \
        .filter(extract('month', Consultation.created_at) == mois) \
        .filter(extract('year', Consultation.created_at) == annee) \
        .all()
    nb_consultations = len(consultations_mois)
    patients_vus = {rv.patient_id for rv in RendezVous.query.filter_by(medecin_id=medecin.id).all()}
    nb_patients = len(patients_vus)
    specialite = medecin.specialite

    # Prochain rendez-vous
    now = datetime.now().time()
    prochain_rdv = RendezVous.query.filter(
        RendezVous.medecin_id == medecin.id,
        RendezVous.date == today,
        RendezVous.heure >= now
    ).order_by(RendezVous.heure).first()

    # Dernier patient consulté
    derniere_consult = Consultation.query \
        .join(RendezVous, Consultation.rendez_vous_id == RendezVous.id) \
        .filter(RendezVous.medecin_id == medecin.id) \
        .order_by(Consultation.created_at.desc()) \
        .first()
    dernier_patient = None
    if derniere_consult:
        dernier_rdv = RendezVous.query.get(derniere_consult.rendez_vous_id)
        dernier_patient = Patient.query.get(dernier_rdv.patient_id) if dernier_rdv else None

    return render_template(
        'medecin/index.html',
        rdv_du_jour=rdv_du_jour,
        nb_consultations=nb_consultations,
        nb_patients=nb_patients,
        specialite=specialite,
        prochain_rdv=prochain_rdv,
        dernier_patient=dernier_patient
    )

@medecin_bp.route('/api/rendezvous')
@login_required
def api_rendezvous():
    medecin = Medecin.query.filter_by(utilisateur_id=current_user.id).first()
    if not medecin:
        return jsonify([])

    rdvs = RendezVous.query.filter_by(medecin_id=medecin.id).all()
    events = []
    for rdv in rdvs:
        color = {
            'programme': '#0d6efd',   # bleu
            'effectue': '#198754',    # vert
            'annule': '#dc3545'       # rouge
        }.get(rdv.statut, '#6c757d')  # gris par défaut

        events.append({
            "id": rdv.id,
            "title": f"{rdv.patient.nom} {rdv.patient.prenom}",
            "start": f"{rdv.date}T{rdv.heure}",
            "end": f"{rdv.date}T{rdv.heure}",
            "color": color,
            "statut": rdv.statut,
            "patient": {
                "nom": rdv.patient.nom,
                "prenom": rdv.patient.prenom,
                "date_naissance": str(rdv.patient.date_naissance),
                "id": rdv.patient.id
            }
        })
    return jsonify(events)

@medecin_bp.route('/calendrier')
@login_required
def calendrier():
    return render_template('medecin/calendrier.html')