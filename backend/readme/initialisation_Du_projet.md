#   structure du projet


projet_python/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Factory (create_app)
│   │   ├── extensions.py        # db, bcrypt, login_manager, migrate
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py          # Model User (SQLAlchemy)
│   │   │   └── post.py          # Model Post (SQLAlchemy)
│   │   ├── routes/
│   │   │   ├── main.py          # Blueprint principal
│   │   │   └── auth.py          # Blueprint auth (login/register/logout)
│   │   ├── services/
│   │   │   └── user_service.py  # Logique métier (create_user, check_password...)
│   │   ├── forms/
│   │   │   ├── auth.py          # LoginForm, RegisterForm (WTForms)
│   │   │   └── post.py          # PostForm
│   │   └── utils/
│   │       └── helpers.py       # Fonctions utilitaires (upload fichier...)
│   ├── config.py                # Dev / Prod config
│   ├── run.py                   # Point d'entrée
│   ├── requirements.txt
│   └── .env
│
└── frontend/
    ├── assets/
    │   ├── css/
    │   ├── js/
    │   └── img/
    ├── pages/                   # Tes pages HTML (Bootstrap)
    └── components/              # Tes composants réutilisables (navbar, footer...)

# Pour demarrer le projet
    cd backend
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python run.py