# Reste à faire – HôpiGest (cahier des charges)

## ✅ Déjà en place (conforme au cahier des charges)

### 4.1 Gestion des utilisateurs
- **Connexion** : email + mot de passe, rôles secrétaire / médecin, redirection selon le rôle.

### 4.2 Gestion des patients (secrétaire)
- Ajout, modification, liste et suppression des patients.
- Champs : nom, prénom, date de naissance, téléphone, adresse, sexe.

### 4.3 Gestion des médecins
- Modèle **Médecin** avec : nom, prénom, spécialité, téléphone, email, lien avec **Utilisateur**.
- Les médecins sont choisis dans les formulaires de rendez-vous (pas de CRUD dédié dans l’interface ; création via le script de seed).

### 4.4 Gestion des rendez-vous (secrétaire)
- Création, modification, suppression, liste.
- Champs : patient, médecin, date, heure, motif, statut (programmé / effectué / annulé).
- Attribution du rendez-vous à un médecin via le formulaire.

### 4.5 Calendrier du médecin
- Liste des rendez-vous du médecin connecté.
- RDV du jour + tous les RDV.
- Clic sur un RDV → accès à la consultation (bouton « Démarrer »).

### 4.6 Consultation médicale
- Page consultation avec infos patient.
- Saisie : symptômes, diagnostic, traitement prescrit, observations.
- Enregistrement dans l’historique (modèle **Consultation**).

### Base de données (modèles)
- **Utilisateur**, **Patient**, **Médecin**, **RendezVous**, **Consultation** avec les champs demandés.

### Interfaces
- Page de connexion, tableau de bord secrétaire, gestion patients, gestion rendez-vous, calendrier médecin, page consultation, historique des consultations.

---

## 🔧 Corrections déjà faites dans le projet

1. **Sécurité** : la route `/medecin/consultation/<id>` vérifie maintenant que le RDV appartient au médecin connecté (sinon redirection + message).
2. **Seed** : script `backend/seed.py` pour créer une secrétaire et deux médecins (voir ci‑dessous).
3. **Statiques** : dossiers `frontend/assets/css` et `frontend/assets/js` avec `style.css` et `main.js` pour éviter les 404.

---

## 📋 À faire de votre côté (obligatoire pour faire tourner l’app)

### 1. Créer la base et les tables
Depuis le dossier `backend/` :

```bash
flask db init
flask db migrate -m "Initial"
flask db upgrade
```

Si vous n’utilisez pas Flask-Migrate, vous pouvez créer les tables au premier lancement avec `db.create_all()` dans un script ou en shell Flask.

### 2. Lancer le seed (utilisateurs + médecins)
Toujours depuis `backend/` :

```bash
python seed.py
```

Cela crée :
- **Secrétaire** : `secretaire@hopital.fr` / `secret123`
- **Médecins** : `jean.martin@hopital.fr` et `sophie.bernard@hopital.fr` / `medecin123`

Sans ce seed, la liste des médecins est vide et la secrétaire ne peut pas créer de rendez-vous.

### 3. Démarrer l’application
Depuis `backend/` :

```bash
python run.py
```

Puis ouvrir l’URL affichée (souvent `http://127.0.0.1:5000`).

---

## 📌 Optionnel / Améliorations (cahier des charges §8)

- **Gestion des médecins dans l’interface** : si vous voulez que la secrétaire (ou un admin) ajoute/modifie des médecins depuis l’app, ajouter des routes + vues « Médecins » (liste, formulaire) et lier chaque médecin à un **Utilisateur** avec rôle `medecin`.
- **Génération d’ordonnance PDF** : ajouter une route (ex. après une consultation) qui génère un PDF (ex. avec ReportLab ou WeasyPrint).
- **Statistiques des consultations** : tableau de bord avec graphiques (nombre de consultations par période, par médecin, etc.).
- **Calendrier interactif** : remplacer ou compléter la liste des RDV par une vraie vue calendrier (ex. FullCalendar ou équivalent en JS).

---

## Résumé

| Bloc du cahier des charges | État |
|----------------------------|------|
| Connexion (email, mot de passe, secrétaire/médecin) | ✅ |
| Secrétaire : patients (CRUD, liste) | ✅ |
| Secrétaire : rendez-vous (CRUD, liste, attribution médecin) | ✅ |
| Médecin : calendrier / liste des RDV | ✅ |
| Médecin : infos patient, consultation, compte rendu | ✅ |
| Historique des consultations | ✅ |
| Modèles BD (Utilisateur, Patient, Médecin, RendezVous, Consultation) | ✅ |
| Sécurité consultation (RDV = médecin connecté) | ✅ (corrigé) |
| Données de test (seed) | ✅ (script fourni) |
| Bonus (PDF, stats, calendrier interactif) | ❌ non fait |

Une fois la base créée et le seed exécuté, l’application couvre les objectifs du cahier des charges ; il ne reste que les bonus si vous souhaitez les ajouter.
