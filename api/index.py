import sys, os

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from app import create_app
from app.extensions import db

app = create_app('production')

with app.app_context():
    db.create_all()
    from app.models import Utilisateur
    if not Utilisateur.query.filter_by(email='admin@cabinet.local').first():
        admin = Utilisateur(nom='Admin', prenom='Super', email='admin@cabinet.local', role='admin')
        admin.set_password('Admin1234!')
        db.session.add(admin)
        db.session.commit()