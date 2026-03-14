from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.decorators import medecin_required
from app.forms.consultation import ConsultationForm
from app.services import rendezvous_service, consultation_service

medecin_bp = Blueprint('medecin', __name__)


# ─── Dashboard / Calendrier ───────────────────────────────────────────────────

@medecin_bp.route('/dashboard')
@login_required
@medecin_required
def dashboard():
    medecin     = current_user.medecin
    rdv_today   = rendezvous_service.get_today_by_medecin(medecin.id)
    tous_rdvs   = rendezvous_service.get_by_medecin(medecin.id)
    consultations = consultation_service.get_by_medecin(medecin.id)
    return render_template('pages/medecin/dashboard.html',
                           medecin=medecin,
                           rdv_today=rdv_today,
                           tous_rdvs=tous_rdvs,
                           total_consultations=len(consultations))


# ─── Consultation ─────────────────────────────────────────────────────────────

@medecin_bp.route('/consultation/<int:rdv_id>', methods=['GET', 'POST'])
@login_required
@medecin_required
def consultation(rdv_id):
    rdv = rendezvous_service.get_by_id(rdv_id)
    if rdv.medecin_id != current_user.medecin.id:
        flash('Ce rendez-vous ne vous est pas attribué.', 'danger')
        return redirect(url_for('medecin.dashboard'))
    form = ConsultationForm()
    if form.validate_on_submit():
        consultation_service.create(rdv, form)
        flash('Consultation enregistrée avec succès.', 'success')
        return redirect(url_for('medecin.dashboard'))
    return render_template('pages/medecin/consultation.html', rdv=rdv, form=form)


# ─── Historique ───────────────────────────────────────────────────────────────

@medecin_bp.route('/historique')
@login_required
@medecin_required
def historique():
    medecin = current_user.medecin
    consultations = consultation_service.get_by_medecin(medecin.id)
    return render_template('pages/medecin/historique.html',
                           consultations=consultations, medecin=medecin)
