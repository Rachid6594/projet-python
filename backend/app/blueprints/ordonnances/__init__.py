"""
Blueprint Ordonnances
=====================
Génération et téléchargement d'ordonnances PDF à partir des consultations.

Routes :
  GET /ordonnances/<consultation_id>/pdf  → Génère et télécharge le PDF de l'ordonnance
"""

from io import BytesIO
from datetime import datetime
from flask import Blueprint, render_template, Response, abort
from flask_login import login_required
from xhtml2pdf import pisa

from app.extensions import db
from app.models.consultation import Consultation
from app.utils.decorators import role_required

ordonnances_bp = Blueprint('ordonnances', __name__)


@ordonnances_bp.route('/<int:consultation_id>/pdf')
@login_required
@role_required('medecin', 'secretaire', 'admin')
def generate_pdf(consultation_id: int):
    """Génère et retourne un PDF d'ordonnance à partir d'une consultation."""

    # Charger la consultation avec ses relations
    consultation = Consultation.query.get_or_404(consultation_id)
    rdv = consultation.rendez_vous
    patient = rdv.patient
    medecin = rdv.medecin

    # Vérifier qu'il y a un traitement
    if not consultation.traitement:
        abort(400)  # Bad Request : pas de traitement à imprimer

    # Rendre le template HTML
    html_string = render_template(
        'ordonnances/ordonnance_pdf.html',
        consultation=consultation,
        rdv=rdv,
        patient=patient,
        medecin=medecin,
        now=datetime.now(),
    )

    # Convertir HTML en PDF avec xhtml2pdf
    pdf_buffer = BytesIO()
    pisa.CreatePDF(
        html_string,
        dest=pdf_buffer,
        link_callback=lambda uri, rel: uri,  # Gérer les liens/images locales si besoin
    )
    pdf_buffer.seek(0)

    # Retourner le PDF en tant que réponse
    filename = f"ordonnance_patient_{patient.id}_{consultation_id}.pdf"
    return Response(
        pdf_buffer.getvalue(),
        mimetype='application/pdf',
        headers={
            'Content-Disposition': f'inline; filename="{filename}"'
        }
    )
