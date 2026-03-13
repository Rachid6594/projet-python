"""
Modèle RendezVous
=================
Représente un rendez-vous planifié entre un patient et un médecin.

Cycle de vie d'un rendez-vous (colonne `statut`) :
  - 'programme' → créé, en attente d'être honoré  (valeur par défaut)
  - 'effectue'  → le patient s'est présenté, la consultation peut être saisie
  - 'annule'    → annulé (patient ou secrétaire)

Un rendez-vous peut donner lieu à au plus une Consultation.
"""

from app.extensions import db


class RendezVous(db.Model):
    __tablename__ = 'rendez_vous'

    # ── Colonnes ──────────────────────────────────────────────────────────
    id = db.Column(db.Integer, primary_key=True)

    # Clés étrangères obligatoires
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patients.id'),
        nullable=False,
    )
    medecin_id = db.Column(
        db.Integer,
        db.ForeignKey('medecins.id'),
        nullable=False,
    )

    date  = db.Column(db.Date, nullable=False)
    heure = db.Column(db.Time, nullable=False)
    motif = db.Column(db.String(255))

    # Statut du rendez-vous : 'programme' | 'effectue' | 'annule'
    statut = db.Column(db.String(20), default='programme', nullable=False)

    # ── Relations ─────────────────────────────────────────────────────────
    # Un rendez-vous est lié à au plus une consultation (relation 1-1)
    # Les backref 'patient' et 'medecin' sont déclarés dans leurs modèles respectifs
    consultation = db.relationship(
        'Consultation',
        backref='rendez_vous',
        uselist=False,
    )

    # ── Représentation ────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f'<RendezVous {self.date} {self.heure} — {self.statut}>'
