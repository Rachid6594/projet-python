from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms.auth import LoginForm
from app.services import auth_service

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = auth_service.authenticate(form.email.data, form.password.data)
        if user:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Bienvenue, {user.prenom} !', 'success')
            if next_page:
                return redirect(next_page)
            if user.role == 'secretaire':
                return redirect(url_for('secretaire.dashboard'))
            return redirect(url_for('medecin.dashboard'))
        flash('Email ou mot de passe incorrect.', 'danger')

    return render_template('pages/auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('auth.login'))
