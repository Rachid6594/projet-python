from datetime import datetime, timezone
from flask_login import UserMixin
from app.extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))


class Utilisateur(db.Model, UserMixin):
    __tablename__ = 'utilisateurs'

    id            = db.Column(db.Integer, primary_key=True)
    nom           = db.Column(db.String(64), nullable=False)
    prenom        = db.Column(db.String(64), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe  = db.Column(db.String(256), nullable=False)
    role          = db.Column(db.String(20), nullable=False)  # 'secretaire' | 'medecin'
    created_at    = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    medecin = db.relationship('Medecin', backref='utilisateur', uselist=False)

    @property
    def nom_complet(self):
        return f'{self.prenom} {self.nom}'

    def is_secretaire(self):
        return self.role == 'secretaire'

    def is_medecin(self):
        return self.role == 'medecin'

    def __repr__(self):
        return f'<Utilisateur {self.email} [{self.role}]>'
