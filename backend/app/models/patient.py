from app.extensions import db


class Patient(db.Model):
    __tablename__ = 'patients'

    id             = db.Column(db.Integer, primary_key=True)
    nom            = db.Column(db.String(64), nullable=False)
    prenom         = db.Column(db.String(64), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    telephone      = db.Column(db.String(20))
    adresse        = db.Column(db.String(200))
    sexe           = db.Column(db.String(1))  # 'M' ou 'F'

    rendezvous = db.relationship('RendezVous', backref='patient', lazy='dynamic',
                                  cascade='all, delete-orphan')

    @property
    def nom_complet(self):
        return f'{self.prenom} {self.nom}'

    def __repr__(self):
        return f'<Patient {self.nom_complet}>'
