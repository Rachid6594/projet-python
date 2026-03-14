from datetime import datetime, timezone
from app.extensions import db


class Consultation(db.Model):
    __tablename__ = 'consultations'

    id             = db.Column(db.Integer, primary_key=True)
    rendezvous_id  = db.Column(db.Integer, db.ForeignKey('rendezvous.id'), nullable=False)
    symptomes      = db.Column(db.Text)
    diagnostic     = db.Column(db.Text, nullable=False)
    traitement     = db.Column(db.Text)
    observations   = db.Column(db.Text)
    created_at     = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Consultation rdv_id={self.rendezvous_id}>'
