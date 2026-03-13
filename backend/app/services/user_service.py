from app.extensions import db, bcrypt
from app.models.user import User


def create_user(username, email, password):
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed)
    db.session.add(user)
    db.session.commit()
    return user


def check_password(user, password):
    return bcrypt.check_password_hash(user.password, password)


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)
