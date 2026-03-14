#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de seed pour initialiser la base de données avec les données de test.
"""

import sys
sys.path.insert(0, '.')

from app import create_app
from app.extensions import db
from app.models.utilisateur import Utilisateur
from app.models.medecin import Medecin
from app.models.patient import Patient

def seed_database():
    """Initialiser la base de données avec les données de test."""

    app = create_app('development')

    with app.app_context():
        # Creer les tables
        db.create_all()
        print("[+] Tables creees")

        # Admin
        admin = Utilisateur(
            nom='Admin',
            prenom='Super',
            email='admin@cabinet.local',
            role='admin'
        )
        admin.set_password('Admin1234!')
        db.session.add(admin)
        db.session.flush()
        print("[+] Admin cree: admin@cabinet.local")

        # Secretaire
        sec = Utilisateur(
            nom='Dupont',
            prenom='Marie',
            email='secretaire@cabinet.local',
            role='secretaire'
        )
        sec.set_password('Secretaire1!')
        db.session.add(sec)
        db.session.flush()
        print("[+] Secretaire creee: secretaire@cabinet.local")

        # Medecin
        med_user = Utilisateur(
            nom='Martin',
            prenom='Jean',
            email='dr.martin@cabinet.local',
            role='medecin'
        )
        med_user.set_password('Medecin1!')
        db.session.add(med_user)
        db.session.flush()

        med = Medecin(
            nom='Martin',
            prenom='Jean',
            specialite='Medecine generale',
            telephone='01 23 45 67 89',
            email='dr.martin@cabinet.local',
            utilisateur_id=med_user.id
        )
        db.session.add(med)
        db.session.flush()
        print("[+] Medecin cree: dr.martin@cabinet.local")

        # Patient
        from datetime import date

        pat = Patient(
            nom='Dupuis',
            prenom='Anne',
            date_naissance=date(1990, 5, 15),
            telephone='06 12 34 56 78',
            adresse='123 Rue de la Paix, 75000 Paris',
            sexe='F'
        )
        db.session.add(pat)

        db.session.commit()
        print("[+] Patient cree: Anne Dupuis")

        print("")
        print("=== Comptes disponibles ===")
        print("Admin: admin@cabinet.local / Admin1234!")
        print("Secretaire: secretaire@cabinet.local / Secretaire1!")
        print("Medecin: dr.martin@cabinet.local / Medecin1!")

if __name__ == '__main__':
    seed_database()
