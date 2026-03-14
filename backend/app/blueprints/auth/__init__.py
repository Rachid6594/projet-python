"""
Blueprint Auth
==============
Gère l'authentification : connexion, déconnexion.

Routes exposées :
  GET/POST  /auth/login   → formulaire de connexion
  GET       /auth/logout  → déconnexion et redirection vers login

Après connexion, la redirection dépend du rôle :
  - 'medecin'    → calendrier des rendez-vous
  - 'secretaire' | 'admin' → liste des patients (dashboard secrétaire)
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.models.utilisateur import Utilisateur

# Création du blueprint ; les templates sont cherchés dans app/templates/
auth_bp = Blueprint('auth', __name__)


# ---------------------------------------------------------------------------
# Connexion
# ---------------------------------------------------------------------------

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Affiche et traite le formulaire de connexion."""

    # Si l'utilisateur est déjà connecté, rediriger directement
    if current_user.is_authenticated:
        return _redirect_after_login(current_user)

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('mot_de_passe', '')
        remember = bool(request.form.get('remember'))

        print(f'DEBUG: POST recu - email={email}, pwd_len={len(password)}')

        utilisateur = Utilisateur.query.filter_by(email=email).first()
        print(f'DEBUG: User found = {utilisateur is not None}')

        if utilisateur:
            pwd_ok = utilisateur.check_password(password)
            print(f'DEBUG: Password OK = {pwd_ok}')
            if pwd_ok:
                login_user(utilisateur, remember=remember)
                flash(f'Bienvenue, {utilisateur.prenom} !', 'success')

                # Respecter l'URL "next" (redirection après page protégée)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)

                return _redirect_after_login(utilisateur)

        # Identifiants incorrects — message générique (sécurité)
        flash('Email ou mot de passe incorrect.', 'danger')

    return render_template('auth/login.html')


# ---------------------------------------------------------------------------
# Déconnexion
# ---------------------------------------------------------------------------

@auth_bp.route('/logout')
@login_required
def logout():
    """Déconnecte l'utilisateur courant et redirige vers la page de login."""
    prenom = current_user.prenom
    logout_user()
    flash(f'À bientôt, {prenom} !', 'info')
    return redirect(url_for('auth.login'))


# ---------------------------------------------------------------------------
# Helpers internes
# ---------------------------------------------------------------------------

def _redirect_after_login(user: Utilisateur):

    if user.role == 'admin':
        return redirect(url_for('admin.index'))

    if user.role == 'medecin':
        return redirect(url_for('medecin.index'))

    if user.role == 'secretaire':
        return redirect(url_for('secretaire.index'))

    return redirect(url_for('auth.login'))
    """Redirige vers la page appropriée selon le rôle de l'utilisateur."""
    if user.role == 'medecin':
        return redirect(url_for('rendez_vous.index'))
    # Secrétaire et admin → gestion des patients
    return redirect(url_for('patients.index'))
