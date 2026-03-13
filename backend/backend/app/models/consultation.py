"""
Modèle Consultation
===================
Représente le compte-rendu médical d'un rendez-vous effectué.

Une consultation est créée par le médecin après avoir reçu le patient.
Elle contient les informations cliniques : symptômes, diagnostic,
traitement prescrit et observations complémentaires.

Contrainte : une consultation est liée à un unique rendez-vous (1-1).
"""

from datetime import datetime

from app.extensions import db


class Consultation(db.Model):
    __tablename__ = 'consultations'

    # ── Colonnes ──────────────────────────────────────────────────────────
    id = db.Column(db.Integer, primary_key=True)

    # Clé étrangère vers le rendez-vous correspondant (obligatoire, unique)
    rendez_vous_id = db.Column(
        db.Integer,
        db.ForeignKey('rendez_vous.id'),
        nullable=False,
        unique=True,   # garantit la relation 1-1 côté base de données
    )

    # Données médicales saisies par le médecin
    symptomes    = db.Column(db.Text)   # symptômes rapportés par le patient
    diagnostic   = db.Column(db.Text)   # diagnostic posé par le médecin
    traitement   = db.Column(db.Text)   # prescription ou plan de traitement
    observations = db.Column(db.Text)   # notes complémentaires libres

    # Horodatage de création automatique
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    # ── Représentation ────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f'<Consultation RDV#{self.rendez_vous_id}>'
