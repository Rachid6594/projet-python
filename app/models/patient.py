"""
Modèle Patient
==============
Représente un patient enregistré dans le système du cabinet médical.

Un patient peut avoir plusieurs rendez-vous au fil du temps.
Il n'est pas un utilisateur de l'application : il n'a pas de compte de connexion.
"""

from datetime import datetime

from app.extensions import db


class Patient(db.Model):
    __tablename__ = 'patients'

    # ── Colonnes ──────────────────────────────────────────────────────────
    id             = db.Column(db.Integer, primary_key=True)
    nom            = db.Column(db.String(100), nullable=False)
    prenom         = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    telephone      = db.Column(db.String(20))
    adresse        = db.Column(db.String(255))
    # Sexe : 'M' (Masculin) ou 'F' (Féminin)
    sexe           = db.Column(db.String(1), nullable=False)
    date_creation  = db.Column(db.DateTime, default=datetime.utcnow)

    # ── Relations ─────────────────────────────────────────────────────────
    # Un patient peut avoir plusieurs rendez-vous (relation 1-N)
    rendez_vous = db.relationship('RendezVous', backref='patient', lazy=True)

    # ── Représentation ────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f'<Patient {self.prenom} {self.nom}>'
