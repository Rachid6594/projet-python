from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.utils.decorators import secretaire_required
from app.forms.patient import PatientForm
from app.forms.rendezvous import RendezVousForm
from app.services import patient_service, rendezvous_service
from app.models.patient import Patient
from app.models.medecin import Medecin
from app.models.rendezvous import RendezVous
from datetime import date

secretaire = Blueprint('secretaire', __name__)


# ─── Dashboard ────────────────────────────────────────────────────────────────

@secretaire.route('/dashboard')
@login_required
@secretaire_required
def dashboard():
    total_patients   = Patient.query.count()
    total_rdv        = RendezVous.query.count()
    rdv_aujourd_hui  = RendezVous.query.filter_by(date=date.today()).count()
    rdv_annules      = RendezVous.query.filter_by(statut='annule').count()
    rdv_recents      = rendezvous_service.get_all()[:5]
    return render_template('pages/secretaire/dashboard.html',
                           total_patients=total_patients,
                           total_rdv=total_rdv,
                           rdv_aujourd_hui=rdv_aujourd_hui,
                           rdv_annules=rdv_annules,
                           rdv_recents=rdv_recents)


# ─── Patients ─────────────────────────────────────────────────────────────────

@secretaire.route('/patients')
@login_required
@secretaire_required
def patients_liste():
    patients = patient_service.get_all()
    return render_template('pages/secretaire/patients_liste.html', patients=patients)


@secretaire.route('/patients/nouveau', methods=['GET', 'POST'])
@login_required
@secretaire_required
def patient_nouveau():
    form = PatientForm()
    if form.validate_on_submit():
        patient_service.create(form)
        flash('Patient enregistré avec succès.', 'success')
        return redirect(url_for('secretaire.patients_liste'))
    return render_template('pages/secretaire/patient_form.html', form=form, titre='Nouveau patient')


@secretaire.route('/patients/<int:patient_id>/modifier', methods=['GET', 'POST'])
@login_required
@secretaire_required
def patient_modifier(patient_id):
    patient = patient_service.get_by_id(patient_id)
    form = PatientForm(obj=patient)
    if form.validate_on_submit():
        patient_service.update(patient, form)
        flash('Patient mis à jour.', 'success')
        return redirect(url_for('secretaire.patients_liste'))
    return render_template('pages/secretaire/patient_form.html', form=form,
                           titre='Modifier le patient', patient=patient)


@secretaire.route('/patients/<int:patient_id>/supprimer', methods=['POST'])
@login_required
@secretaire_required
def patient_supprimer(patient_id):
    patient = patient_service.get_by_id(patient_id)
    patient_service.delete(patient)
    flash('Patient supprimé.', 'warning')
    return redirect(url_for('secretaire.patients_liste'))


# ─── Rendez-vous ──────────────────────────────────────────────────────────────

@secretaire.route('/rendezvous')
@login_required
@secretaire_required
def rendezvous_liste():
    rdvs = rendezvous_service.get_all()
    return render_template('pages/secretaire/rendezvous_liste.html', rdvs=rdvs)


@secretaire.route('/rendezvous/nouveau', methods=['GET', 'POST'])
@login_required
@secretaire_required
def rendezvous_nouveau():
    form = RendezVousForm()
    form.patient_id.choices = [(p.id, p.nom_complet) for p in Patient.query.order_by(Patient.nom).all()]
    form.medecin_id.choices = [(m.id, m.nom_complet) for m in Medecin.query.order_by(Medecin.nom).all()]
    if form.validate_on_submit():
        rendezvous_service.create(form)
        flash('Rendez-vous créé avec succès.', 'success')
        return redirect(url_for('secretaire.rendezvous_liste'))
    return render_template('pages/secretaire/rendezvous_form.html', form=form,
                           titre='Nouveau rendez-vous')


@secretaire.route('/rendezvous/<int:rdv_id>/modifier', methods=['GET', 'POST'])
@login_required
@secretaire_required
def rendezvous_modifier(rdv_id):
    rdv = rendezvous_service.get_by_id(rdv_id)
    form = RendezVousForm(obj=rdv)
    form.patient_id.choices = [(p.id, p.nom_complet) for p in Patient.query.order_by(Patient.nom).all()]
    form.medecin_id.choices = [(m.id, m.nom_complet) for m in Medecin.query.order_by(Medecin.nom).all()]
    if form.validate_on_submit():
        rendezvous_service.update(rdv, form)
        flash('Rendez-vous mis à jour.', 'success')
        return redirect(url_for('secretaire.rendezvous_liste'))
    return render_template('pages/secretaire/rendezvous_form.html', form=form,
                           titre='Modifier le rendez-vous', rdv=rdv)


@secretaire.route('/rendezvous/<int:rdv_id>/supprimer', methods=['POST'])
@login_required
@secretaire_required
def rendezvous_supprimer(rdv_id):
    rdv = rendezvous_service.get_by_id(rdv_id)
    rendezvous_service.delete(rdv)
    flash('Rendez-vous supprimé.', 'warning')
    return redirect(url_for('secretaire.rendezvous_liste'))
