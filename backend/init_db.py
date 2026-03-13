"""
Script d'initialisation de la base de données
==============================================
Ce script :
  1. Crée toutes les tables SQLAlchemy (si elles n'existent pas)
  2. Crée un compte administrateur par défaut
  3. Insère des données de test (seed) : médecins, patients, rendez-vous

Utilisation :
    cd backend
    python init_db.py

    # Ou avec l'environnement de production :
    FLASK_ENV=production python init_db.py
"""

import os
from datetime import date, time

from app import create_app
from app.extensions import db
from app.models import (  # noqa — déclenche la détection de tous les modèles
    Consultation,
    Medecin,
    Patient,
    RendezVous,
    Utilisateur,
)

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

# Identifiants du compte admin par défaut (à modifier après la 1ère connexion)
ADMIN_EMAIL    = os.environ.get('ADMIN_EMAIL',    'admin@cabinet.local')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin1234!')
ADMIN_NOM      = 'Admin'
ADMIN_PRENOM   = 'Super'


def create_tables(app):
    """Crée le dossier instance/ si absent, puis toutes les tables SQLAlchemy."""
    # SQLite ne peut pas créer le fichier .db si le dossier parent n'existe pas
    instance_dir = os.path.join(os.path.dirname(__file__), 'instance')
    os.makedirs(instance_dir, exist_ok=True)

    with app.app_context():
        db.create_all()
        print('[✓] Tables créées (ou déjà existantes).')


def seed_admin(app):
    """Crée le compte administrateur par défaut s'il n'existe pas encore."""
    with app.app_context():
        existant = Utilisateur.query.filter_by(email=ADMIN_EMAIL).first()
        if existant:
            print(f'[~] Compte admin déjà existant : {ADMIN_EMAIL}')
            return

        admin = Utilisateur(
            nom    = ADMIN_NOM,
            prenom = ADMIN_PRENOM,
            email  = ADMIN_EMAIL,
            role   = 'admin',
        )
        admin.set_password(ADMIN_PASSWORD)
        db.session.add(admin)
        db.session.commit()
        print(f'[✓] Compte admin créé : {ADMIN_EMAIL} / {ADMIN_PASSWORD}')
        print('    → Pensez à changer le mot de passe après la première connexion !')


def seed_test_data(app):
    """Insère des données de test représentatives (idempotent)."""
    with app.app_context():

        # ── Secrétaire de test ────────────────────────────────────────────
        if not Utilisateur.query.filter_by(email='secretaire@cabinet.local').first():
            sec = Utilisateur(
                nom='Dupont', prenom='Marie',
                email='secretaire@cabinet.local', role='secretaire',
            )
            sec.set_password('Secretaire1!')
            db.session.add(sec)
            db.session.flush()   # obtenir l'id avant le commit
            print('[✓] Secrétaire de test créée : secretaire@cabinet.local / Secretaire1!')

        # ── Médecin de test ───────────────────────────────────────────────
        if not Utilisateur.query.filter_by(email='dr.martin@cabinet.local').first():
            user_med = Utilisateur(
                nom='Martin', prenom='Jean',
                email='dr.martin@cabinet.local', role='medecin',
            )
            user_med.set_password('Medecin1!')
            db.session.add(user_med)
            db.session.flush()

            fiche_med = Medecin(
                nom='Martin', prenom='Jean',
                specialite='Médecine générale',
                telephone='01 23 45 67 89',
                email='dr.martin@cabinet.local',
                user_id=user_med.id,
            )
            db.session.add(fiche_med)
            db.session.flush()
            print('[✓] Médecin de test créé : dr.martin@cabinet.local / Medecin1!')

            # ── Patients de test ──────────────────────────────────────────
            if Patient.query.count() == 0:
                patients = [
                    Patient(nom='Durand',  prenom='Alice',  date_naissance=date(1985, 3, 15),
                            telephone='06 11 22 33 44', sexe='F', adresse='12 rue de la Paix, Paris'),
                    Patient(nom='Lefebvre', prenom='Pierre', date_naissance=date(1972, 7, 22),
                            telephone='06 55 66 77 88', sexe='M', adresse='8 avenue des Fleurs, Lyon'),
                    Patient(nom='Bernard', prenom='Sophie', date_naissance=date(1990, 11, 5),
                            telephone='07 99 88 77 66', sexe='F', adresse='3 impasse du Moulin, Marseille'),
                ]
                db.session.add_all(patients)
                db.session.flush()
                print(f'[✓] {len(patients)} patients de test insérés.')

                # ── Rendez-vous de test ────────────────────────────────────
                rdv1 = RendezVous(
                    patient_id=patients[0].id,
                    medecin_id=fiche_med.id,
                    date=date(2025, 6, 10),
                    heure=time(9, 0),
                    motif='Consultation de routine',
                    statut='effectue',
                )
                rdv2 = RendezVous(
                    patient_id=patients[1].id,
                    medecin_id=fiche_med.id,
                    date=date(2025, 6, 11),
                    heure=time(10, 30),
                    motif='Douleurs lombaires',
                    statut='programme',
                )
                db.session.add_all([rdv1, rdv2])
                db.session.flush()
                print('[✓] 2 rendez-vous de test insérés.')

                # ── Consultation liée au RDV effectué ─────────────────────
                consult = Consultation(
                    rendez_vous_id=rdv1.id,
                    symptomes='Fatigue, légère fièvre (37.8°C)',
                    diagnostic='Infection virale bénigne',
                    traitement='Repos, paracétamol 1g x3/jour pendant 5 jours',
                    observations='À revoir si fièvre persiste au-delà de 48h',
                )
                db.session.add(consult)
                print('[✓] 1 consultation de test insérée.')

        db.session.commit()
        print('[✓] Données de test validées en base.')


# ─────────────────────────────────────────────────────────────────────────────
# Point d'entrée
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    env = os.environ.get('FLASK_ENV', 'development')
    print(f'\n=== Initialisation de la base de données ({env}) ===\n')

    application = create_app(env)

    create_tables(application)
    seed_admin(application)
    seed_test_data(application)

    print('\n=== Initialisation terminée ===\n')
    print('Comptes disponibles :')
    print(f'  Admin      : {ADMIN_EMAIL} / {ADMIN_PASSWORD}')
    print('  Secrétaire : secretaire@cabinet.local / Secretaire1!')
    print('  Médecin    : dr.martin@cabinet.local  / Medecin1!')
