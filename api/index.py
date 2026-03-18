import sys
import os

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

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
    from app.models import Utilisateur
    if not Utilisateur.query.filter_by(email='admin@cabinet.local').first():
        db.session.add(Utilisateur(
            nom='Admin', prenom='Super',
            email='admin@cabinet.local', role='admin',
            mot_de_passe=generate_password_hash('Admin1234!'),
        ))
    if not Utilisateur.query.filter_by(email='secretaire@cabinet.local').first():
        db.session.add(Utilisateur(
            nom='Kabore', prenom='Marie',
            email='secretaire@cabinet.local', role='secretaire',
            mot_de_passe=generate_password_hash('Secretaire1!'),
        ))
    db.session.commit()