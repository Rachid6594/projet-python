from app.extensions import db
from app.models.patient import Patient


def get_all():
    return Patient.query.order_by(Patient.nom).all()


def get_by_id(patient_id):
    return Patient.query.get_or_404(patient_id)


def create(form):
    patient = Patient(
        nom=form.nom.data,
        prenom=form.prenom.data,
        date_naissance=form.date_naissance.data,
        telephone=form.telephone.data,
        adresse=form.adresse.data,
        sexe=form.sexe.data
    )
    db.session.add(patient)
    db.session.commit()
    return patient


def update(patient, form):
    patient.nom = form.nom.data
    patient.prenom = form.prenom.data
    patient.date_naissance = form.date_naissance.data
    patient.telephone = form.telephone.data
    patient.adresse = form.adresse.data
    patient.sexe = form.sexe.data
    db.session.commit()
    return patient


def delete(patient):
    db.session.delete(patient)
    db.session.commit()
