# HôpiGest — Système de Gestion des Rendez-vous Hospitaliers

Application web Flask pour gérer les rendez-vous médicaux, consultations et patients dans un environnement hospitalier.

## 📋 Fonctionnalités

### Secrétaire
- ✅ Gestion complète des patients (CRUD)
- ✅ Création et modification des rendez-vous
- ✅ Attribution des rendez-vous aux médecins
- ✅ Tableau de bord avec statistiques

### Médecin
- ✅ Consultation du calendrier personnel
- ✅ Liste des rendez-vous assignés
- ✅ Effectuer des consultations médicales
- ✅ Enregistrement des diagnostics et traitements
- ✅ Historique des consultations

## 🏗️ Architecture

```
projet_python/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   ├── routes/          # Flask blueprints
│   │   ├── services/        # Logique métier
│   │   ├── forms/           # WTForms
│   │   ├── utils/           # Utilitaires & décorateurs
│   │   ├── __init__.py      # Factory pattern
│   │   └── extensions.py    # Extensions Flask
│   ├── config.py            # Configuration
│   ├── run.py               # Point d'entrée
│   ├── seed.py              # Données de test
│   └── requirements.txt      # Dépendances
│
└── frontend/
    ├── pages/               # Templates Jinja2
    │   ├── auth/
    │   ├── secretaire/
    │   └── medecin/
    ├── components/          # Composants réutilisables
    └── assets/              # CSS, JS, images
        ├── css/style.css
        └── js/main.js
```

## 🚀 Démarrage rapide

### 1. Installation

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# ou source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### 2. Initialiser la base de données

```bash
# Depuis backend/
python seed.py
```

Cela crée :
- **Secrétaire** : `secretaire@hopital.fr` / `secret123`
- **Médecin 1** : `jean.martin@hopital.fr` / `medecin123`
- **Médecin 2** : `sophie.bernard@hopital.fr` / `medecin123`

### 3. Lancer l'application

```bash
# Depuis backend/
python run.py
```

Accédez à : `http://localhost:5000`

## 🔑 Identifiants par défaut

| Rôle      | Email                         | Mot de passe |
|-----------|-------------------------------|-------------|
| Secrétaire | `secretaire@hopital.fr`      | `secret123` |
| Médecin   | `jean.martin@hopital.fr`      | `medecin123` |
| Médecin   | `sophie.bernard@hopital.fr`   | `medecin123` |

## 📦 Technologies

- **Backend** : Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend** : Bootstrap 5, Jinja2
- **Base de données** : SQLite (dev), MySQL/PostgreSQL (prod)
- **Authentification** : Flask-Login, Flask-Bcrypt

## 📝 Modèles de données

### Utilisateur
- `id`, `nom`, `prenom`, `email`, `mot_de_passe`, `role` (secretaire|medecin)

### Patient
- `id`, `nom`, `prenom`, `date_naissance`, `sexe`, `telephone`, `adresse`

### Médecin
- `id`, `nom`, `prenom`, `specialite`, `telephone`, `email`, `utilisateur_id` (FK)

### RendezVous
- `id`, `patient_id`, `medecin_id`, `date`, `heure`, `motif`, `statut` (programme|effectue|annule)

### Consultation
- `id`, `rendezvous_id`, `symptomes`, `diagnostic`, `traitement`, `observations`

## 🔐 Sécurité

- Authentification par email/mot de passe
- Hachage des mots de passe avec bcrypt
- Décorateurs pour le contrôle d'accès par rôle
- Protection CSRF sur tous les formulaires
- Sessions sécurisées avec Flask-Login

## 📌 Routes principales

### Authentification
- `GET/POST /auth/login` — Connexion
- `GET /auth/logout` — Déconnexion

### Secrétaire
- `GET /secretaire/dashboard` — Tableau de bord
- `GET/POST /secretaire/patients` — Gestion des patients
- `GET/POST /secretaire/rendezvous` — Gestion des rendez-vous

### Médecin
- `GET /medecin/dashboard` — Calendrier des RDV
- `GET/POST /medecin/consultation/<rdv_id>` — Effectuer une consultation
- `GET /medecin/historique` — Historique des consultations

## 📂 Fichiers importants

- `backend/app/__init__.py` — Initialisation Flask avec factory pattern
- `backend/seed.py` — Script pour peupler la base avec des données de test
- `frontend/base.html` — Template de base avec sidebar et topbar
- `frontend/assets/css/style.css` — Styles personnalisés

## ⚙️ Variables d'environnement

Édite `backend/.env` :

```env
FLASK_APP=run.py
FLASK_DEBUG=1
SECRET_KEY=ta-clé-secrète
DATABASE_URL=  # Laisse vide pour SQLite en dev
```

## 🐛 Développement

Pour modifier le code :

1. Les changements sont appliqués automatiquement (mode debug activé)
2. Les migrations de base de données : `flask db migrate && flask db upgrade`
3. Tests : À ajouter

## 📚 Documentation supplémentaire

- Consulte `RESTE_A_FAIRE.md` pour les fonctionnalités bonus prévues
- Flask : https://flask.palletsprojects.com/
- SQLAlchemy : https://docs.sqlalchemy.org/
- Bootstrap 5 : https://getbootstrap.com/

---

**Développé avec Flask et Bootstrap** 🏥
