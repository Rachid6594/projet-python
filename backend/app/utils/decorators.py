"""
Décorateurs de protection des routes
=====================================
Fournit des décorateurs à combiner avec @login_required de Flask-Login.

Usage :
    @app.route('/admin')
    @login_required
    @role_required('admin')
    def admin_panel():
        ...

    @app.route('/espace-medical')
    @login_required
    @role_required('medecin', 'admin')
    def espace_medical():
        ...
"""

from functools import wraps

from flask import abort
from flask_login import current_user


def role_required(*roles: str):
    """
    Décorateur vérifiant que l'utilisateur connecté possède l'un des rôles
    passés en argument.

    - Renvoie HTTP 401 si l'utilisateur n'est pas authentifié.
    - Renvoie HTTP 403 si l'utilisateur est authentifié mais n'a pas le rôle.

    Note : utiliser APRÈS @login_required pour un message d'erreur plus propre
    (Flask-Login redirige automatiquement vers la page de login en cas de 401).
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Sécurité supplémentaire : vérifier l'authentification
            if not current_user.is_authenticated:
                abort(401)

            # Vérifier que le rôle de l'utilisateur est dans la liste autorisée
            if current_user.role not in roles:
                abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator
