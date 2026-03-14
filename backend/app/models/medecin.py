from app.extensions import db


class Medecin(db.Model):
    __tablename__ = 'medecins'

    id             = db.Column(db.Integer, primary_key=True)
    nom            = db.Column(db.String(64), nullable=False)
    prenom         = db.Column(db.String(64), nullable=False)
    specialite     = db.Column(db.String(100))
    telephone      = db.Column(db.String(20))
    email          = db.Column(db.String(120))
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'))

    rendezvous = db.relationship('RendezVous', backref='medecin', lazy='dynamic')

    @property
    def nom_complet(self):
        return f'Dr. {self.prenom} {self.nom}'

    def __repr__(self):
        return f'<Medecin {self.nom_complet}>'
