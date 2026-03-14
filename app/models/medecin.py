"""
Modèle Medecin
==============
Représente la fiche professionnelle d'un médecin du cabinet.

Chaque médecin est obligatoirement lié à un compte Utilisateur (via user_id)
dont le rôle doit être 'medecin'. Cette relation permet à un médecin de
se connecter à l'application et d'accéder à son propre calendrier.
"""

from app.extensions import db


class Medecin(db.Model):
    __tablename__ = 'medecins'

    # ── Colonnes ──────────────────────────────────────────────────────────
    id         = db.Column(db.Integer, primary_key=True)
    nom        = db.Column(db.String(100), nullable=False)
    prenom     = db.Column(db.String(100), nullable=False)
    specialite = db.Column(db.String(150), nullable=False)
    telephone  = db.Column(db.String(20))
    email      = db.Column(db.String(150))

    # Clé étrangère vers le compte Utilisateur associé (obligatoire)
    user_id    = db.Column(
        db.Integer,
        db.ForeignKey('utilisateurs.id'),
        nullable=False,
    )

    # ── Relations ─────────────────────────────────────────────────────────
    # Un médecin peut avoir plusieurs rendez-vous (relation 1-N)
    rendez_vous = db.relationship('RendezVous', backref='medecin', lazy=True)


    def __repr__(self) -> str:
        return f'<Médecin Dr. {self.prenom} {self.nom} — {self.specialite}>'
