"""
Script de seed : crée une secrétaire et des médecins pour pouvoir utiliser l'application.
À lancer une fois la base créée : depuis backend/ faire
    python seed.py
ou depuis la racine du projet :
    cd backend && python seed.py
"""
import sys
import os

# Ajouter le répertoire backend au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db, bcrypt
from app.models.utilisateur import Utilisateur
from app.models.medecin import Medecin


def run_seed():
    app = create_app('development')
    with app.app_context():
        if Utilisateur.query.filter_by(email='secretaire@hopital.fr').first():
            print('Données déjà présentes (secrétaire existe). Rien à faire.')
            return

        # Secrétaire
        sec = Utilisateur(
            nom='Dupont',
            prenom='Marie',
            email='secretaire@hopital.fr',
            mot_de_passe=bcrypt.generate_password_hash('secret123').decode('utf-8'),
            role='secretaire'
        )
        db.session.add(sec)

        # Médecin 1 + utilisateur
        u1 = Utilisateur(
            nom='Martin',
            prenom='Jean',
            email='jean.martin@hopital.fr',
            mot_de_passe=bcrypt.generate_password_hash('medecin123').decode('utf-8'),
            role='medecin'
        )
        db.session.add(u1)
        db.session.flush()
        m1 = Medecin(
            nom='Martin',
            prenom='Jean',
            specialite='Médecine générale',
            telephone='01 23 45 67 89',
            email='jean.martin@hopital.fr',
            utilisateur_id=u1.id
        )
        db.session.add(m1)

        # Médecin 2 + utilisateur
        u2 = Utilisateur(
            nom='Bernard',
            prenom='Sophie',
            email='sophie.bernard@hopital.fr',
            mot_de_passe=bcrypt.generate_password_hash('medecin123').decode('utf-8'),
            role='medecin'
        )
        db.session.add(u2)
        db.session.flush()
        m2 = Medecin(
            nom='Bernard',
            prenom='Sophie',
            specialite='Cardiologie',
            telephone='01 98 76 54 32',
            email='sophie.bernard@hopital.fr',
            utilisateur_id=u2.id
        )
        db.session.add(m2)

        db.session.commit()
        print('Seed OK.')
        print('  Secrétaire : secretaire@hopital.fr / secret123')
        print('  Médecin 1  : jean.martin@hopital.fr / medecin123')
        print('  Médecin 2  : sophie.bernard@hopital.fr / medecin123')


if __name__ == '__main__':
    run_seed()
