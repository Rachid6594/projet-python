"""
Blueprint Admin
===============
Panneau d'administration réservé exclusivement au rôle 'admin'.

Plus-value du compte admin par rapport à la secrétaire :
  - Créer, modifier et supprimer des comptes utilisateurs (médecins, secrétaires)
  - Voir tous les comptes applicatifs
  - Réinitialiser les mots de passe

Routes :
  GET   /admin/                              → tableau de bord (stats)
  GET   /admin/utilisateurs/                → liste + modals créer / modifier / supprimer
  POST  /admin/utilisateurs/nouveau         → traite la création (soumis depuis modal)
  POST  /admin/utilisateurs/<id>/modifier   → traite la modification (soumis depuis modal)
  POST  /admin/utilisateurs/<id>/supprimer  → supprime le compte
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.utils.decorators import role_required

admin_bp = Blueprint('admin', __name__)


# ---------------------------------------------------------------------------
# Tableau de bord
# ---------------------------------------------------------------------------

@admin_bp.route('/')
@login_required
@role_required('admin')
def index():
    """Vue d'ensemble : compteurs utilisateurs, médecins, patients."""
    from app.models.medecin     import Medecin
    from app.models.patient     import Patient
    from app.models.utilisateur import Utilisateur

    stats = {
        'utilisateurs': Utilisateur.query.count(),
        'medecins':     Medecin.query.count(),
        'patients':     Patient.query.count(),
        'secretaires':  Utilisateur.query.filter_by(role='secretaire').count(),
    }
    return render_template('admin/index.html', stats=stats)


# ---------------------------------------------------------------------------
# Liste des comptes — page principale avec les 3 modals
# ---------------------------------------------------------------------------

@admin_bp.route('/utilisateurs/')
@login_required
@role_required('admin')
def utilisateurs():
    """Affiche tous les comptes et fournit les modals créer / modifier / supprimer."""
    from app.models.utilisateur import Utilisateur
    comptes = Utilisateur.query.order_by(Utilisateur.role, Utilisateur.nom).all()
    return render_template('admin/utilisateurs.html', comptes=comptes)


# ---------------------------------------------------------------------------
# Créer un compte (POST depuis le modal de création)
# ---------------------------------------------------------------------------

@admin_bp.route('/utilisateurs/nouveau', methods=['POST'])
@login_required
@role_required('admin')
def nouveau_utilisateur():
    """Crée un compte utilisateur. Si rôle médecin, crée aussi la fiche Medecin."""
    from app.extensions         import db
    from app.models.medecin     import Medecin
    from app.models.utilisateur import Utilisateur

    nom        = request.form.get('nom', '').strip()
    prenom     = request.form.get('prenom', '').strip()
    email      = request.form.get('email', '').strip().lower()
    role       = request.form.get('role', '')
    password   = request.form.get('mot_de_passe', '')
    specialite = request.form.get('specialite', '').strip()

    if Utilisateur.query.filter_by(email=email).first():
        flash('Cet email est déjà utilisé.', 'danger')
        return redirect(url_for('admin.utilisateurs'))

    utilisateur = Utilisateur(nom=nom, prenom=prenom, email=email, role=role)
    utilisateur.set_password(password)
    db.session.add(utilisateur)
    db.session.flush()

    # Créer la fiche professionnelle si le rôle est médecin
    if role == 'medecin':
        fiche = Medecin(
            nom=nom, prenom=prenom,
            specialite=specialite or 'Non renseignée',
            email=email,
            user_id=utilisateur.id,
        )
        db.session.add(fiche)

    db.session.commit()
    flash(f'Compte créé : {prenom} {nom} ({role}).', 'success')
    return redirect(url_for('admin.utilisateurs'))


# ---------------------------------------------------------------------------
# Modifier un compte (POST depuis le modal de modification)
# ---------------------------------------------------------------------------

@admin_bp.route('/utilisateurs/<int:user_id>/modifier', methods=['POST'])
@login_required
@role_required('admin')
def modifier_utilisateur(user_id: int):
    """
    Met à jour nom, prénom, email et rôle.
    Le mot de passe n'est changé que si un nouveau est fourni dans le formulaire.
    """
    from app.extensions         import db
    from app.models.utilisateur import Utilisateur

    utilisateur = Utilisateur.query.get_or_404(user_id)

    utilisateur.nom    = request.form.get('nom', '').strip()
    utilisateur.prenom = request.form.get('prenom', '').strip()
    utilisateur.email  = request.form.get('email', '').strip().lower()
    utilisateur.role   = request.form.get('role', utilisateur.role)

    # Changer le mot de passe uniquement si un nouveau est saisi
    nouveau_mdp = request.form.get('mot_de_passe', '').strip()
    if nouveau_mdp:
        utilisateur.set_password(nouveau_mdp)

    # Synchroniser la fiche Medecin si ce compte est un médecin
    if utilisateur.medecin:
        utilisateur.medecin.nom    = utilisateur.nom
        utilisateur.medecin.prenom = utilisateur.prenom
        utilisateur.medecin.email  = utilisateur.email

    db.session.commit()
    flash(f'Compte de {utilisateur.prenom} {utilisateur.nom} mis à jour.', 'success')
    return redirect(url_for('admin.utilisateurs'))


# ---------------------------------------------------------------------------
# Supprimer un compte (POST depuis le modal de suppression)
# ---------------------------------------------------------------------------

@admin_bp.route('/utilisateurs/<int:user_id>/supprimer', methods=['POST'])
@login_required
@role_required('admin')
def supprimer_utilisateur(user_id: int):
    """Supprime un compte utilisateur. Empêche l'admin de se supprimer lui-même."""
    from app.extensions         import db
    from app.models.utilisateur import Utilisateur

    utilisateur = Utilisateur.query.get_or_404(user_id)

    if utilisateur.id == current_user.id:
        flash('Vous ne pouvez pas supprimer votre propre compte.', 'warning')
        return redirect(url_for('admin.utilisateurs'))

    nom_complet = f'{utilisateur.prenom} {utilisateur.nom}'
    db.session.delete(utilisateur)
    db.session.commit()
    flash(f'Compte de {nom_complet} supprimé.', 'info')
    return redirect(url_for('admin.utilisateurs'))
