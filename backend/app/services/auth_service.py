from app.extensions import bcrypt
from app.models.utilisateur import Utilisateur


def authenticate(email, password):
    user = Utilisateur.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.mot_de_passe, password):
        return user
    return None


def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')
