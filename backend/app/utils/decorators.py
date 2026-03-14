from functools import wraps
from flask import abort
from flask_login import current_user


def secretaire_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'secretaire':
            abort(403)
        return f(*args, **kwargs)
    return decorated


def medecin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'medecin':
            abort(403)
        return f(*args, **kwargs)
    return decorated
