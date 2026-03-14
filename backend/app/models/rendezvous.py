from datetime import datetime, timezone
from app.extensions import db


class RendezVous(db.Model):
    __tablename__ = 'rendezvous'

    id         = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    medecin_id = db.Column(db.Integer, db.ForeignKey('medecins.id'), nullable=False)
    date       = db.Column(db.Date, nullable=False)
    heure      = db.Column(db.Time, nullable=False)
    motif      = db.Column(db.String(200))
    statut     = db.Column(db.String(20), default='programme')  # programme | effectue | annule
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    consultation = db.relationship('Consultation', backref='rendezvous', uselist=False,
                                    cascade='all, delete-orphan')

    def __repr__(self):
        return f'<RendezVous {self.date} {self.heure} statut={self.statut}>'
