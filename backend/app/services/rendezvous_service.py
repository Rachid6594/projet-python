from datetime import date
from app.extensions import db
from app.models.rendezvous import RendezVous


def get_all():
    return RendezVous.query.order_by(RendezVous.date, RendezVous.heure).all()


def get_by_id(rdv_id):
    return RendezVous.query.get_or_404(rdv_id)


def get_today():
    return RendezVous.query.filter_by(date=date.today()).all()


def get_by_medecin(medecin_id):
    return RendezVous.query.filter_by(medecin_id=medecin_id)\
        .order_by(RendezVous.date, RendezVous.heure).all()


def get_today_by_medecin(medecin_id):
    return RendezVous.query.filter_by(medecin_id=medecin_id, date=date.today())\
        .order_by(RendezVous.heure).all()


def create(form):
    rdv = RendezVous(
        patient_id=form.patient_id.data,
        medecin_id=form.medecin_id.data,
        date=form.date.data,
        heure=form.heure.data,
        motif=form.motif.data,
        statut='programme'
    )
    db.session.add(rdv)
    db.session.commit()
    return rdv


def update(rdv, form):
    rdv.patient_id = form.patient_id.data
    rdv.medecin_id = form.medecin_id.data
    rdv.date = form.date.data
    rdv.heure = form.heure.data
    rdv.motif = form.motif.data
    rdv.statut = form.statut.data
    db.session.commit()
    return rdv


def annuler(rdv):
    rdv.statut = 'annule'
    db.session.commit()


def delete(rdv):
    db.session.delete(rdv)
    db.session.commit()
