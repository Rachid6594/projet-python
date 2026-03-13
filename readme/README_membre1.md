# Partie 1 — Structure, Modèles & Authentification

**Membre :** Membre 1
**Partie :** 1.1 · 1.2 · 1.3

---

## Sommaire

1. [Ce qui a été réalisé](#ce-qui-a-été-réalisé)
2. [Structure des fichiers](#structure-des-fichiers)
3. [Architecture 3 espaces](#architecture-3-espaces)
4. [1.1 — Structure du projet Flask](#11--structure-du-projet-flask)
5. [1.2 — Modèles de la base de données](#12--modèles-de-la-base-de-données)
6. [1.3 — Système d'authentification](#13--système-dauthentification)
7. [Panneau d'administration](#panneau-dadministration)
8. [Démarrage rapide](#lancer-le-projet)
9. [Comptes de test](#comptes-de-test)
10. [Guide pour les autres membres](#guide-pour-les-autres-membres)

---

## Ce qui a été réalisé

| # | Tâche | Fichier(s) |
|---|-------|-----------|
| 1.1.1 | Structure en Blueprints (8 blueprints) | `app/blueprints/` |
| 1.1.2 | Configuration dev / prod | `config.py`, `.env` |
| 1.1.3 | Variables d'environnement | `backend/.env` + `python-dotenv` |
| 1.1.4 | Layout Jinja2 (`base.html`) | `frontend/templates/base.html` |
| 1.1.5 | Intégration Bootstrap 5 | `base.html` (CDN) |
| 1.2.1 | Modèle `Utilisateur` | `app/models/utilisateur.py` |
| 1.2.2 | Modèle `Patient` | `app/models/patient.py` |
| 1.2.3 | Modèle `Medecin` | `app/models/medecin.py` |
| 1.2.4 | Modèle `RendezVous` | `app/models/rendez_vous.py` |
| 1.2.5 | Modèle `Consultation` | `app/models/consultation.py` |
| 1.2.6 | Migrations + seed | `init_db.py` |
| 1.3.1 | Flask-Login | `app/extensions.py`, `app/models/utilisateur.py` |
| 1.3.2 | Hachage Werkzeug | `Utilisateur.set_password()` / `check_password()` |
| 1.3.3 | Page de connexion | `frontend/templates/auth/login.html` |
| 1.3.4 | Déconnexion + redirection par rôle | `app/blueprints/auth/__init__.py` |
| 1.3.5 | Décorateurs `@login_required` / `@role_required` | `app/utils/decorators.py` |
| 1.3.6 | Compte admin par défaut | `init_db.py` → `seed_admin()` |
| 1.4.1 | Blueprint admin + tableau de bord | `app/blueprints/admin/__init__.py` |
| 1.4.2 | Gestion des comptes utilisateurs | `admin/utilisateurs.html` (modals CRUD) |
| 1.4.3 | Architecture 3 espaces distincts | `admin/`, `secretaire/`, `medecin/` |
| 1.4.4 | Redirections par rôle après connexion | `app/__init__.py` → `index()` |

---

## Structure des fichiers

```
projet-python/
│
├── frontend/
│   ├── components/                      ← composants Jinja2 réutilisables
│   │   ├── _navbar.html                 ← navigation adaptée au rôle connecté
│   │   ├── _user_menu.html              ← bouton déconnexion visible
│   │   ├── _flash_messages.html         ← alertes Bootstrap avec icônes
│   │   └── _footer.html                 ← pied de page (année dynamique)
│   │
│   └── templates/                       ← pages Jinja2
│       ├── base.html                    ← layout Bootstrap 5
│       ├── auth/
│       │   └── login.html               ← formulaire email / mot de passe
│       │
│       ├── admin/                       ← ESPACE ADMIN (Membre 1)
│       │   ├── index.html               ← tableau de bord (stats + raccourcis)
│       │   └── utilisateurs.html        ← gestion des comptes (CRUD modals)
│       │
│       ├── secretaire/                  ← ESPACE SECRÉTAIRE (Membres 2 & 3)
│       │   └── index.html               ← page d'accueil secrétaire
│       │
│       ├── medecin/                     ← ESPACE MÉDECIN (Membre 4)
│       │   └── index.html               ← page d'accueil médecin
│       │
│       ├── patients/
│       │   └── index.html               ← placeholder pour Membre 2
│       ├── medecins/
│       │   └── index.html               ← placeholder pour Membre 3
│       ├── rendez_vous/
│       │   └── index.html               ← placeholder pour Membres 3 & 4
│       └── consultations/
│           └── index.html               ← placeholder pour Membre 4
│
└── backend/
    ├── .env                             ← SECRET_KEY, FLASK_ENV, DATABASE_URL
    ├── config.py                        ← DevelopmentConfig / ProductionConfig
    ├── run.py                           ← point d'entrée Flask
    ├── init_db.py                       ← création tables + données de test
    │
    └── app/
        ├── __init__.py                  ← factory create_app() + ChoiceLoader
        ├── extensions.py                ← db, login_manager, migrate
        │
        ├── models/
        │   ├── __init__.py              ← import centralisé pour Alembic
        │   ├── utilisateur.py           ← Utilisateur (UserMixin, hachage mdp)
        │   ├── patient.py               ← Patient
        │   ├── medecin.py               ← Medecin (FK → Utilisateur)
        │   ├── rendez_vous.py           ← RendezVous (FK → Patient, Medecin)
        │   └── consultation.py          ← Consultation (FK → RendezVous, unique)
        │
        ├── blueprints/
        │   ├── auth/                    ← login, logout, redirection par rôle
        │   ├── admin/                   ← tableau de bord + gestion comptes
        │   ├── secretaire/              ← accueil espace secrétaire
        │   ├── medecin/                 ← accueil espace médecin
        │   ├── patients/                ← CRUD patients (Membre 2)
        │   ├── medecins/                ← annuaire médecins (Membre 3)
        │   ├── rendez_vous/             ← gestion RDV (Membre 3 & 4)
        │   └── consultations/           ← comptes-rendus (Membre 4)
        │
        └── utils/
            └── decorators.py            ← @role_required(*roles)
```

---

## Architecture 3 espaces

Le projet est divisé en **3 espaces totalement indépendants** :

```
/admin/       → réservé à l'administrateur (Membre 1)
/secretaire/  → espace secrétaire (Membres 2 & 3)
/medecin/     → espace médecin connecté (Membre 4)
```

### Redirection automatique après connexion

Définie dans [`backend/app/__init__.py`](../backend/app/__init__.py) route `/` :

| Rôle | Redirection |
|------|-------------|
| `admin` | `/admin/` |
| `medecin` | `/medecin/` |
| `secretaire` | `/secretaire/` |

### Séparation des responsabilités

| Espace | Blueprints concernés | Membres |
|--------|---------------------|---------|
| `admin/` | `admin` | Membre 1 |
| `secretaire/` | `secretaire`, `patients`, `medecins`, `rendez_vous` | Membres 2 & 3 |
| `medecin/` | `medecin`, `consultations`, `rendez_vous` | Membre 4 |

---

## 1.1 — Structure du projet Flask

### Application Factory

L'application est créée via le pattern **Application Factory** (`create_app()`) dans [`backend/app/__init__.py`](../backend/app/__init__.py). Cela permet d'instancier Flask avec des configurations différentes (dev, prod, test).

### Blueprints

8 blueprints organisent les routes de l'application :

| Blueprint | Préfixe URL | Rôles autorisés | Responsable |
|-----------|-------------|-----------------|-------------|
| `auth` | `/auth` | tous | Membre 1 |
| `admin` | `/admin` | admin | Membre 1 |
| `secretaire` | `/secretaire` | secrétaire, admin | Membre 1 (accueil) |
| `medecin` | `/medecin` | médecin | Membre 1 (accueil) |
| `patients` | `/patients` | secrétaire, admin | Membre 2 |
| `medecins` | `/medecins` | secrétaire, admin | Membre 3 |
| `rendez_vous` | `/rendez-vous` | secrétaire, admin, médecin | Membres 3 & 4 |
| `consultations` | `/consultations` | médecin | Membre 4 |

### Configuration

Le fichier [`config.py`](../backend/config.py) définit deux environnements :

```python
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/dev.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```

Les variables sensibles (`SECRET_KEY`, `DATABASE_URL`) sont chargées depuis [`.env`](../backend/.env) via **python-dotenv**.

### Templates & Composants

Le layout Bootstrap 5 est découpé en composants Jinja2 réutilisables via `{% include %}` :

- **`base.html`** — layout principal, inclut les 3 composants ci-dessous
- **`_navbar.html`** — navigation adaptée au rôle de l'utilisateur connecté
- **`_flash_messages.html`** — alertes dismissibles avec icône selon la catégorie
- **`_footer.html`** — pied de page avec année injectée par un context processor

Le `ChoiceLoader` de Jinja2 est configuré dans `create_app()` pour chercher les templates dans `frontend/templates/` **et** les composants dans `frontend/components/`.

---

## 1.2 — Modèles de la base de données

### Diagramme des relations

```
Utilisateur (1) ──────── (0..1) Medecin
                                   │
Patient (1) ──┐                    │
              ├── (N) RendezVous (N)┘
              └────────────┘
                    │
              (0..1) Consultation
```

### Détail des modèles

#### `Utilisateur` — [`utilisateur.py`](../backend/app/models/utilisateur.py)

| Colonne | Type | Contrainte |
|---------|------|-----------|
| `id` | Integer | PK |
| `nom` / `prenom` | String(100) | NOT NULL |
| `email` | String(150) | UNIQUE, NOT NULL |
| `mot_de_passe` | String(256) | NOT NULL (hashé) |
| `role` | String(20) | `'secretaire'` \| `'medecin'` \| `'admin'` |
| `date_creation` | DateTime | default=utcnow |

Implémente `UserMixin` (Flask-Login) et fournit `set_password()` / `check_password()` via **Werkzeug**.

#### `Patient` — [`patient.py`](../backend/app/models/patient.py)

| Colonne | Type | Contrainte |
|---------|------|-----------|
| `id` | Integer | PK |
| `nom` / `prenom` | String(100) | NOT NULL |
| `date_naissance` | Date | NOT NULL |
| `telephone` | String(20) | nullable |
| `adresse` | String(255) | nullable |
| `sexe` | String(1) | `'M'` ou `'F'` |
| `date_creation` | DateTime | default=utcnow |

#### `Medecin` — [`medecin.py`](../backend/app/models/medecin.py)

| Colonne | Type | Contrainte |
|---------|------|-----------|
| `id` | Integer | PK |
| `nom` / `prenom` | String(100) | NOT NULL |
| `specialite` | String(150) | NOT NULL |
| `telephone` / `email` | String | nullable |
| `user_id` | Integer | FK → `utilisateurs.id`, NOT NULL |

#### `RendezVous` — [`rendez_vous.py`](../backend/app/models/rendez_vous.py)

| Colonne | Type | Contrainte |
|---------|------|-----------|
| `id` | Integer | PK |
| `patient_id` | Integer | FK → `patients.id` |
| `medecin_id` | Integer | FK → `medecins.id` |
| `date` / `heure` | Date / Time | NOT NULL |
| `motif` | String(255) | nullable |
| `statut` | String(20) | `'programme'` \| `'effectue'` \| `'annule'` |

#### `Consultation` — [`consultation.py`](../backend/app/models/consultation.py)

| Colonne | Type | Contrainte |
|---------|------|-----------|
| `id` | Integer | PK |
| `rendez_vous_id` | Integer | FK → `rendez_vous.id`, UNIQUE |
| `symptomes` | Text | nullable |
| `diagnostic` | Text | nullable |
| `traitement` | Text | nullable |
| `observations` | Text | nullable |
| `date_creation` | DateTime | default=utcnow |

> La contrainte `unique=True` sur `rendez_vous_id` garantit la relation **1-1** directement en base.

### Migrations

Flask-Migrate (Alembic) est configuré. Tous les modèles sont importés dans [`models/__init__.py`](../backend/app/models/__init__.py) pour qu'Alembic les détecte automatiquement.

```bash
flask db init      # (une seule fois)
flask db migrate -m "initial"
flask db upgrade
```

---

## 1.3 — Système d'authentification

### Flask-Login

Le callback `load_user()` est défini dans [`utilisateur.py`](../backend/app/models/utilisateur.py) et recharge l'utilisateur depuis la session à chaque requête.

### Connexion (`/auth/login`)

- Récupère email + mot de passe depuis le formulaire POST
- Vérifie via `Utilisateur.check_password()` (Werkzeug `check_password_hash`)
- Appelle `login_user()` avec l'option "se souvenir de moi"
- Redirige selon le rôle vers l'espace correspondant
- Message d'erreur générique (pas de distinction email/mdp pour la sécurité)

### Déconnexion (`/auth/logout`)

- Protégée par `@login_required`
- Appelle `logout_user()` et redirige vers la page de login
- Bouton de déconnexion **directement visible** dans la navbar (non caché dans un dropdown)

### Décorateur `@role_required`

Défini dans [`utils/decorators.py`](../backend/app/utils/decorators.py) :

```python
@patients_bp.route('/')
@login_required
@role_required('secretaire', 'admin')
def index():
    ...
```

- Renvoie **HTTP 401** si non authentifié
- Renvoie **HTTP 403** si rôle non autorisé

### Compte administrateur par défaut

Créé par le script [`init_db.py`](../backend/init_db.py) via la fonction `seed_admin()`. Les identifiants sont configurables via variables d'environnement :

```bash
ADMIN_EMAIL=admin@cabinet.local     # valeur par défaut
ADMIN_PASSWORD=Admin1234!           # valeur par défaut
```

---

## Panneau d'administration

L'espace admin (`/admin/`) est réservé au rôle `admin` et comprend :

### Tableau de bord (`/admin/`)

- Cartes de statistiques : nombre total d'utilisateurs, médecins, secrétaires
- Boutons de raccourcis vers les fonctions principales

### Gestion des comptes (`/admin/utilisateurs`)

Tableau listant tous les comptes avec pour chaque utilisateur :
- Nom complet, email, rôle (badge coloré), date de création
- **Bouton Modifier** → ouvre un modal pré-rempli avec les données du compte
- **Bouton Supprimer** → ouvre un modal de confirmation avec le nom du compte
- Le compte admin connecté affiche "votre compte" (protection contre auto-suppression)

#### Routes admin disponibles

| Méthode | URL | Action |
|---------|-----|--------|
| GET | `/admin/` | Tableau de bord |
| GET | `/admin/utilisateurs` | Liste des comptes |
| POST | `/admin/utilisateurs/nouveau` | Créer un compte |
| POST | `/admin/utilisateurs/<id>/modifier` | Modifier un compte |
| POST | `/admin/utilisateurs/<id>/supprimer` | Supprimer un compte |

> Quand un médecin est créé/modifié via l'admin, sa fiche `Medecin` en base est automatiquement synchronisée.

---

## Lancer le projet

### Prérequis

- **Python 3.10+** installé sur la machine
- **Git** pour cloner le dépôt

---

### Étape 1 — Cloner le dépôt

```bash
git clone <url-du-depot>
cd projet-python
```

---

### Étape 2 — Créer l'environnement virtuel

```bash
cd backend
python -m venv venv
```

Activer l'environnement :

```bash
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# Linux / macOS
source venv/bin/activate
```

> Le terminal doit afficher `(venv)` en début de ligne pour confirmer l'activation.

---

### Étape 3 — Installer les dépendances

```bash
pip install -r requirements.txt
```

Dépendances installées :

| Package | Version | Rôle |
|---------|---------|------|
| Flask | 3.1.0 | Framework web |
| Flask-SQLAlchemy | 3.1.1 | ORM base de données |
| Flask-Migrate | 4.0.7 | Migrations Alembic |
| Flask-Login | 0.6.3 | Gestion des sessions |
| Flask-Bcrypt | 1.0.1 | Hachage (extensions) |
| Flask-WTF | 1.2.1 | Formulaires + CSRF |
| Werkzeug | 3.1.3 | Hachage des mots de passe |
| python-dotenv | 1.0.1 | Variables d'environnement |

---

### Étape 4 — Configurer les variables d'environnement

Le fichier `.env` est déjà présent dans `backend/`. Vérifier son contenu :

```bash
# backend/.env
SECRET_KEY=change-me-in-production-use-a-long-random-string
FLASK_ENV=development
FLASK_DEBUG=1
```

> En production, remplacer `SECRET_KEY` par une chaîne aléatoire longue et définir `DATABASE_URL`.

---

### Étape 5 — Initialiser la base de données

```bash
# Toujours depuis le dossier backend/ avec (venv) actif
python init_db.py
```

Ce script effectue :
1. Création de toutes les tables SQLAlchemy (`db.create_all()`)
2. Création du compte **admin** par défaut
3. Insertion des données de test (secrétaire, médecin, patients, RDV, consultation)

Sortie attendue :
```
=== Initialisation de la base de données (development) ===

[✓] Tables créées (ou déjà existantes).
[✓] Compte admin créé : admin@cabinet.local / Admin1234!
[✓] Secrétaire de test créée : secretaire@cabinet.local / Secretaire1!
[✓] Médecin de test créé : dr.martin@cabinet.local / Medecin1!
[✓] 3 patients de test insérés.
[✓] 2 rendez-vous de test insérés.
[✓] 1 consultation de test insérée.
[✓] Données de test validées en base.

=== Initialisation terminée ===
```

---

### Étape 6 — Lancer le serveur

```bash
python run.py
```

L'application est accessible à l'adresse :

```
http://127.0.0.1:5000
```

La route `/` redirige automatiquement vers `/auth/login`, puis vers l'espace correspondant au rôle.

---

### Utiliser Flask-Migrate (migrations)

Si le schéma des modèles est modifié, générer et appliquer une migration :

```bash
# Initialiser Alembic (une seule fois, dossier migrations/ déjà présent)
flask db init

# Générer une migration depuis les changements de modèles
flask db migrate -m "description du changement"

# Appliquer la migration à la base
flask db upgrade

# Revenir à la migration précédente si besoin
flask db downgrade
```

---

### Résumé des commandes

```bash
cd backend
python -m venv venv && venv\Scripts\activate   # créer + activer le venv
pip install -r requirements.txt                # installer les dépendances
python init_db.py                              # créer la DB + seed
python run.py                                  # lancer le serveur
# → http://127.0.0.1:5000
```

---

## Comptes de test

| Rôle | Email | Mot de passe | Redirection après connexion |
|------|-------|--------------|----------------------------|
| Admin | `admin@cabinet.local` | `Admin1234!` | `/admin/` |
| Secrétaire | `secretaire@cabinet.local` | `Secretaire1!` | `/secretaire/` |
| Médecin | `dr.martin@cabinet.local` | `Medecin1!` | `/medecin/` |

> **Important :** changer les mots de passe avant tout déploiement en production.

---

## Guide pour les autres membres

### Ce que Membre 1 a préparé pour vous

Tout ce dont vous avez besoin est déjà en place :
- Les **modèles SQLAlchemy** (`Patient`, `Medecin`, `RendezVous`, `Consultation`) sont définis et migrés
- Les **blueprints** sont enregistrés et les préfixes URL sont fixés
- Les **décorateurs** `@login_required` et `@role_required` sont prêts à l'emploi
- Les **données de test** sont insérées via `init_db.py`
- Les **templates placeholders** existent déjà dans les bons dossiers

### Membre 2 — Gestion des patients

- Blueprint : [`backend/app/blueprints/patients/__init__.py`](../backend/app/blueprints/patients/__init__.py)
- Templates : [`frontend/templates/patients/`](../frontend/templates/patients/)
- Préfixe URL : `/patients`
- Rôles autorisés : `secretaire`, `admin`
- Modèle disponible : `from app.models.patient import Patient`

```python
# Exemple d'utilisation du décorateur
@patients_bp.route('/')
@login_required
@role_required('secretaire', 'admin')
def index():
    patients = Patient.query.order_by(Patient.nom).all()
    return render_template('patients/index.html', patients=patients)
```

### Membre 3 — Médecins & Rendez-vous

- Blueprint médecins : [`backend/app/blueprints/medecins/__init__.py`](../backend/app/blueprints/medecins/__init__.py)
- Blueprint rendez-vous : [`backend/app/blueprints/rendez_vous/__init__.py`](../backend/app/blueprints/rendez_vous/__init__.py)
- Templates : [`frontend/templates/medecins/`](../frontend/templates/medecins/) et [`frontend/templates/rendez_vous/`](../frontend/templates/rendez_vous/)
- Préfixes URL : `/medecins`, `/rendez-vous`
- Modèles disponibles : `Medecin`, `RendezVous`, `Patient`

> Note : la liste des médecins dans `/medecins` est l'annuaire global (espace secrétaire). Ne pas confondre avec `/medecin` (espace personnel du médecin connecté, géré par Membre 4).

### Membre 4 — Consultations & Espace médecin

- Blueprint médecin : [`backend/app/blueprints/medecin/__init__.py`](../backend/app/blueprints/medecin/__init__.py)
- Blueprint consultations : [`backend/app/blueprints/consultations/__init__.py`](../backend/app/blueprints/consultations/__init__.py)
- Templates : [`frontend/templates/medecin/`](../frontend/templates/medecin/) et [`frontend/templates/consultations/`](../frontend/templates/consultations/)
- Préfixes URL : `/medecin`, `/consultations`
- Rôle autorisé : `medecin`
- Modèles disponibles : `RendezVous`, `Consultation`, `Medecin`, `Patient`

```python
# Récupérer le médecin connecté
from app.models.medecin import Medecin
from flask_login import current_user

medecin = Medecin.query.filter_by(user_id=current_user.id).first()
```

### Règles communes

1. **Ne jamais modifier** `base.html`, `_navbar.html`, `_flash_messages.html`, `_footer.html` sans coordination avec Membre 1
2. **Ne jamais modifier** les modèles sans créer une migration Flask-Migrate
3. **Toujours utiliser** `@login_required` + `@role_required` sur chaque route protégée
4. **Ajouter vos templates** dans le sous-dossier correspondant à votre espace (`secretaire/`, `medecin/`)
5. **Flash messages** : utiliser `flash('message', 'success')` / `flash('message', 'danger')` pour les retours utilisateur
