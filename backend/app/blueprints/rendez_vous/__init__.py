"""
Blueprint Rendez-vous
=====================
Gestion des rendez-vous : prise, modification, annulation, calendrier.

- Secrétaires et admins : gestion globale (tous les médecins)
- Médecins              : accès en lecture à leur propre calendrier
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from datetime import datetime

from app.extensions import db
from app.utils.decorators import role_required
from app.models.rendez_vous import RendezVous
from app.models.medecin import Medecin
from app.models.patient import Patient

rendez_vous_bp = Blueprint('rendez_vous', __name__)


# ---------------------------------------------------------------------------
# Fonction de détection de conflits
# ---------------------------------------------------------------------------

def check_time_conflict(medecin_id, date, heure, exclude_id=None):
    """
    Vérifie si un médecin a déjà un rendez-vous à ce créneau.

    Args:
        medecin_id: ID du médecin
        date: Date du rendez-vous
        heure: Heure du rendez-vous
        exclude_id: ID du rendez-vous à exclure (pour les modifications)

    Returns:
        True si conflit existe, False sinon
    """
    query = RendezVous.query.filter(
        RendezVous.medecin_id == medecin_id,
        RendezVous.date == date,
        RendezVous.heure == heure,
        RendezVous.statut != 'annule'
    )

    if exclude_id:
        query = query.filter(RendezVous.id != exclude_id)

    return query.first() is not None


# ---------------------------------------------------------------------------
# Calendrier / liste des rendez-vous
# ---------------------------------------------------------------------------

@rendez_vous_bp.route('/')
@login_required
@role_required('secretaire', 'admin', 'medecin')
def index():
    """
    Affiche les rendez-vous :
      - Médecin    → uniquement les siens
      - Secrétaire → tous les rendez-vous
    """
    if current_user.role == 'medecin':
        # Récupérer la fiche médecin liée au compte connecté
        medecin = Medecin.query.filter_by(user_id=current_user.id).first_or_404()
        rdvs = (RendezVous.query
                .filter_by(medecin_id=medecin.id)
                .order_by(RendezVous.date, RendezVous.heure)
                .all())
    else:
        rdvs = RendezVous.query.order_by(RendezVous.date, RendezVous.heure).all()

    return render_template('rendez_vous/index.html', rendez_vous=rdvs)


# ---------------------------------------------------------------------------
# Création rendez-vous
# ---------------------------------------------------------------------------

@rendez_vous_bp.route('/nouveau', methods=['GET', 'POST'])
@login_required
@role_required('secretaire', 'admin')
def create():
    """Créer un nouveau rendez-vous."""

    if request.method == "POST":

        medecin_id = int(request.form["medecin_id"])
        patient_id = int(request.form["patient_id"])
        date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        heure = datetime.strptime(request.form["heure"], "%H:%M").time()

        # Vérifier si le créneau est disponible
        if check_time_conflict(medecin_id, date, heure):
            flash("Ce créneau est déjà réservé pour ce médecin", "danger")
            patients = Patient.query.order_by(Patient.nom).all()
            medecins = Medecin.query.order_by(Medecin.nom).all()
            return render_template(
                "rendez_vous/create.html",
                patients=patients,
                medecins=medecins
            )

        # Créer le rendez-vous
        rdv = RendezVous(
            patient_id=patient_id,
            medecin_id=medecin_id,
            date=date,
            heure=heure,
            motif=request.form.get("motif", ""),
            statut="programme"
        )

        db.session.add(rdv)
        db.session.commit()

        flash("Rendez-vous créé avec succès", "success")

        return redirect(url_for("rendez_vous.index"))

    # GET : afficher le formulaire
    patients = Patient.query.order_by(Patient.nom).all()
    medecins = Medecin.query.order_by(Medecin.nom).all()

    return render_template(
        "rendez_vous/create.html",
        patients=patients,
        medecins=medecins
    )


# ---------------------------------------------------------------------------
# Détail rendez-vous
# ---------------------------------------------------------------------------

@rendez_vous_bp.route('/<int:id>')
@login_required
@role_required('secretaire', 'admin', 'medecin')
def show(id):
    """Affiche le détail d'un rendez-vous."""

    rdv = RendezVous.query.get_or_404(id)

    # Si médecin, vérifier que c'est bien son RDV
    if current_user.role == 'medecin':
        medecin = Medecin.query.filter_by(user_id=current_user.id).first_or_404()
        if rdv.medecin_id != medecin.id:
            flash("Accès non autorisé", "danger")
            return redirect(url_for("rendez_vous.index"))

    return render_template("rendez_vous/show.html", rdv=rdv)


# ---------------------------------------------------------------------------
# Modifier rendez-vous
# ---------------------------------------------------------------------------

@rendez_vous_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('secretaire', 'admin')
def edit(id):
    """Modifier un rendez-vous."""

    rdv = RendezVous.query.get_or_404(id)

    # Empêcher la modification si déjà effectué
    if rdv.statut == 'effectue':
        flash("Impossible de modifier un rendez-vous déjà effectué", "warning")
        return redirect(url_for("rendez_vous.show", id=id))

    if request.method == "POST":

        medecin_id = int(request.form["medecin_id"])
        patient_id = int(request.form["patient_id"])
        date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        heure = datetime.strptime(request.form["heure"], "%H:%M").time()

        # Vérifier les conflits (en excluant le RDV actuel)
        if check_time_conflict(medecin_id, date, heure, exclude_id=id):
            flash("Ce créneau est déjà réservé pour ce médecin", "danger")
            patients = Patient.query.order_by(Patient.nom).all()
            medecins = Medecin.query.order_by(Medecin.nom).all()
            return render_template(
                "rendez_vous/edit.html",
                rdv=rdv,
                patients=patients,
                medecins=medecins
            )

        # Mettre à jour le rendez-vous
        rdv.patient_id = patient_id
        rdv.medecin_id = medecin_id
        rdv.date = date
        rdv.heure = heure
        rdv.motif = request.form.get("motif", "")

        db.session.commit()

        flash("Rendez-vous modifié avec succès", "success")

        return redirect(url_for("rendez_vous.show", id=id))

    # GET : afficher le formulaire pré-rempli
    patients = Patient.query.order_by(Patient.nom).all()
    medecins = Medecin.query.order_by(Medecin.nom).all()

    return render_template(
        "rendez_vous/edit.html",
        rdv=rdv,
        patients=patients,
        medecins=medecins
    )


# ---------------------------------------------------------------------------
# Annuler rendez-vous
# ---------------------------------------------------------------------------

@rendez_vous_bp.route('/<int:id>/annuler', methods=['POST'])
@login_required
@role_required('secretaire', 'admin')
def cancel(id):
    """Annuler un rendez-vous."""

    rdv = RendezVous.query.get_or_404(id)

    # Empêcher l'annulation si déjà effectué
    if rdv.statut == 'effectue':
        flash("Impossible d'annuler un rendez-vous déjà effectué", "warning")
        return redirect(url_for("rendez_vous.show", id=id))

    rdv.statut = 'annule'
    db.session.commit()

    flash("Rendez-vous annulé avec succès", "info")

    return redirect(url_for("rendez_vous.index"))
