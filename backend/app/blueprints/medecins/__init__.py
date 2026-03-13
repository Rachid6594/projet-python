"""
Blueprint Médecins
==================
Gestion des fiches médecins : liste, création, modification, suppression.

Accès réservé aux rôles : 'secretaire', 'admin'.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app.extensions import db
from app.utils.decorators import role_required
from app.models.medecin import Medecin
from app.models.utilisateur import Utilisateur

medecins_bp = Blueprint('medecins', __name__)


# ---------------------------------------------------------------------------
# Liste des médecins
# ---------------------------------------------------------------------------

@medecins_bp.route('/')
@login_required
@role_required('secretaire', 'admin')
def index():
    """Affiche la liste de tous les médecins du cabinet."""
    medecins = Medecin.query.order_by(Medecin.nom).all()
    return render_template('medecins/index.html', medecins=medecins)


# ---------------------------------------------------------------------------
# Création médecin
# ---------------------------------------------------------------------------

@medecins_bp.route('/nouveau', methods=['GET', 'POST'])
@login_required
@role_required('secretaire', 'admin')
def create():
    """Créer un nouveau médecin et son compte utilisateur associé."""

    if request.method == "POST":

        # Vérifier si l'email existe déjà
        email = request.form.get("email", "").strip()
        if email and Utilisateur.query.filter_by(email=email).first():
            flash("Un compte avec cet email existe déjà", "danger")
            return render_template("medecins/create.html")

        # Créer le compte utilisateur
        utilisateur = Utilisateur(
            nom=request.form["nom"],
            prenom=request.form["prenom"],
            email=email,
            role="medecin"
        )

        # Définir un mot de passe par défaut ou celui fourni
        mot_de_passe = request.form.get("mot_de_passe", "Medecin123!")
        utilisateur.set_password(mot_de_passe)

        db.session.add(utilisateur)
        db.session.flush()  # Pour obtenir l'ID de l'utilisateur

        # Créer la fiche médecin
        medecin = Medecin(
            nom=request.form["nom"],
            prenom=request.form["prenom"],
            specialite=request.form["specialite"],
            telephone=request.form.get("telephone", ""),
            email=email,
            user_id=utilisateur.id
        )

        db.session.add(medecin)
        db.session.commit()

        flash("Médecin ajouté avec succès", "success")

        return redirect(url_for("medecins.index"))

    return render_template("medecins/create.html")


# ---------------------------------------------------------------------------
# Détail médecin
# ---------------------------------------------------------------------------

@medecins_bp.route('/<int:id>')
@login_required
@role_required('secretaire', 'admin')
def show(id):
    """Affiche le profil détaillé d'un médecin."""

    medecin = Medecin.query.get_or_404(id)

    from datetime import date
    from app.models.rendez_vous import RendezVous

    # RDV à venir
    rdv_a_venir = (
        RendezVous.query
        .filter(RendezVous.medecin_id == id, RendezVous.date >= date.today())
        .order_by(RendezVous.date.asc())
        .all()
    )

    # Statistiques
    total_rdv = RendezVous.query.filter_by(medecin_id=id).count()
    rdv_effectues = RendezVous.query.filter_by(medecin_id=id, statut='effectue').count()

    return render_template(
        "medecins/show.html",
        medecin=medecin,
        rdv_a_venir=rdv_a_venir,
        total_rdv=total_rdv,
        rdv_effectues=rdv_effectues
    )


# ---------------------------------------------------------------------------
# Modifier médecin
# ---------------------------------------------------------------------------

@medecins_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('secretaire', 'admin')
def edit(id):
    """Modifier les informations d'un médecin."""

    medecin = Medecin.query.get_or_404(id)
    utilisateur = medecin.utilisateur

    if request.method == "POST":

        # Vérifier si l'email a changé et n'est pas déjà utilisé
        new_email = request.form.get("email", "").strip()
        if new_email != utilisateur.email:
            if Utilisateur.query.filter_by(email=new_email).first():
                flash("Cet email est déjà utilisé par un autre compte", "danger")
                return render_template("medecins/edit.html", medecin=medecin)

        # Mettre à jour la fiche médecin
        medecin.nom = request.form["nom"]
        medecin.prenom = request.form["prenom"]
        medecin.specialite = request.form["specialite"]
        medecin.telephone = request.form.get("telephone", "")
        medecin.email = new_email

        # Mettre à jour le compte utilisateur associé
        utilisateur.nom = request.form["nom"]
        utilisateur.prenom = request.form["prenom"]
        utilisateur.email = new_email

        # Mettre à jour le mot de passe si fourni
        new_password = request.form.get("mot_de_passe", "").strip()
        if new_password:
            utilisateur.set_password(new_password)

        db.session.commit()

        flash("Médecin modifié avec succès", "success")

        return redirect(url_for("medecins.index"))

    return render_template(
        "medecins/edit.html",
        medecin=medecin
    )


# ---------------------------------------------------------------------------
# Supprimer médecin
# ---------------------------------------------------------------------------

@medecins_bp.route('/<int:id>/supprimer', methods=['POST'])
@login_required
@role_required('secretaire', 'admin')
def delete(id):
    """Supprimer un médecin et son compte utilisateur associé."""

    medecin = Medecin.query.get_or_404(id)
    utilisateur = medecin.utilisateur

    # Vérifier si le médecin a des rendez-vous
    from app.models.rendez_vous import RendezVous
    rdv_count = RendezVous.query.filter_by(medecin_id=id).count()

    if rdv_count > 0:
        flash(f"Impossible de supprimer : ce médecin a {rdv_count} rendez-vous associé(s)", "danger")
        return redirect(url_for("medecins.index"))

    # Supprimer le médecin et son compte utilisateur
    db.session.delete(medecin)
    db.session.delete(utilisateur)
    db.session.commit()

    flash("Médecin supprimé avec succès", "info")

    return redirect(url_for("medecins.index"))
