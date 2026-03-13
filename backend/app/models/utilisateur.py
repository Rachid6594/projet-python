"""
Modèle Utilisateur
==================
Représente un compte applicatif pouvant appartenir à l'un des trois rôles :
  - 'secretaire' : accès à la gestion des patients et des rendez-vous
  - 'medecin'    : accès à son calendrier et aux consultations
  - 'admin'      : accès complet (création de comptes, configuration)

Ce modèle implémente UserMixin de Flask-Login afin de gérer
automatiquement les propriétés is_authenticated, is_active, etc.
"""

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


# ---------------------------------------------------------------------------
# Callback Flask-Login
# Flask-Login appelle cette fonction à chaque requête pour recharger
# l'utilisateur depuis son identifiant stocké en session.
# ---------------------------------------------------------------------------
@login_manager.user_loader
def load_user(user_id: str):
    return Utilisateur.query.get(int(user_id))


# ---------------------------------------------------------------------------
# Modèle
# ---------------------------------------------------------------------------
class Utilisateur(UserMixin, db.Model):
    __tablename__ = 'utilisateurs'

    # ── Colonnes ──────────────────────────────────────────────────────────
    id            = db.Column(db.Integer, primary_key=True)
    nom           = db.Column(db.String(100), nullable=False)
    prenom        = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False)
    mot_de_passe  = db.Column(db.String(256), nullable=False)
    # Rôles autorisés : 'secretaire' | 'medecin' | 'admin'
    role          = db.Column(db.String(20), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    # ── Relations ─────────────────────────────────────────────────────────
    # Un utilisateur de rôle 'medecin' est associé à une fiche Medecin (1-1)
    medecin = db.relationship('Medecin', backref='utilisateur', uselist=False)

    # ── Méthodes mot de passe ─────────────────────────────────────────────

    def set_password(self, password: str) -> None:
        """Hache le mot de passe en clair et le stocke."""
        self.mot_de_passe = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Vérifie un mot de passe en clair contre le hash stocké."""
        return check_password_hash(self.mot_de_passe, password)

    # ── Représentation ────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f'<Utilisateur {self.prenom} {self.nom} ({self.role})>'
