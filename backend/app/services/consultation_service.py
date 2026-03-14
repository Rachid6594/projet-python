from app.extensions import db
from app.models.consultation import Consultation
from app.models.rendezvous import RendezVous


def create(rdv, form):
    consultation = Consultation(
        rendezvous_id=rdv.id,
        symptomes=form.symptomes.data,
        diagnostic=form.diagnostic.data,
        traitement=form.traitement.data,
        observations=form.observations.data
    )
    rdv.statut = 'effectue'
    db.session.add(consultation)
    db.session.commit()
    return consultation


def get_by_patient(patient_id):
    return Consultation.query\
        .join(RendezVous)\
        .filter(RendezVous.patient_id == patient_id)\
        .order_by(Consultation.created_at.desc())\
        .all()


def get_by_medecin(medecin_id):
    return Consultation.query\
        .join(RendezVous)\
        .filter(RendezVous.medecin_id == medecin_id)\
        .order_by(Consultation.created_at.desc())\
        .all()
