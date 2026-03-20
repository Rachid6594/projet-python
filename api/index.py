import sys
import os

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from datetime import date, time
from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db

app = create_app('production')

_db_initialized = False

@app.before_request
def init_db_once():
    global _db_initialized
    if _db_initialized:
        return
    _db_initialized = True
    db.create_all()

    from app.models.utilisateur import Utilisateur
    from app.models.medecin import Medecin
    from app.models.patient import Patient
    from app.models.rendez_vous import RendezVous

    # Ne seeder que si la base est vide
    if Utilisateur.query.first():
        return

    # --- Utilisateurs ---
    admin = Utilisateur(
        nom='Admin', prenom='Super',
        email='admin@cabinet.local', role='admin',
        mot_de_passe=generate_password_hash('Admin1234!'),
    )
    db.session.add(admin)

    secretaire = Utilisateur(
        nom='Dupont', prenom='Marie',
        email='secretaire@cabinet.local', role='secretaire',
        mot_de_passe=generate_password_hash('Secretaire1!'),
    )
    db.session.add(secretaire)

    med_user = Utilisateur(
        nom='Martin', prenom='Jean',
        email='dr.martin@cabinet.local', role='medecin',
        mot_de_passe=generate_password_hash('Medecin1!'),
    )
    db.session.add(med_user)
    db.session.flush()

    # --- Medecin (profil lie au compte) ---
    medecin = Medecin(
        nom='Martin', prenom='Jean',
        specialite='Medecine generale',
        telephone='01 23 45 67 89',
        email='dr.martin@cabinet.local',
        utilisateur_id=med_user.id,
    )
    db.session.add(medecin)
    db.session.flush()

    # --- Patient ---
    patient = Patient(
        nom='Dupuis', prenom='Anne',
        date_naissance=date(1990, 5, 15),
        telephone='06 12 34 56 78',
        adresse='123 Rue de la Paix, 75000 Paris',
        sexe='F',
    )
    db.session.add(patient)
    db.session.flush()

    # --- Rendez-vous de demonstration ---
    today = date.today()
    rdv = RendezVous(
        patient_id=patient.id,
        medecin_id=medecin.id,
        date=today,
        heure=time(10, 0),
        motif='Consultation de routine',
        statut='programme',
    )
    db.session.add(rdv)

    db.session.commit()
