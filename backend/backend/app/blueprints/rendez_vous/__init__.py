"""
Blueprint Rendez-vous
=====================
Gestion des rendez-vous : prise, modification, annulation, calendrier.

- Secrétaires et admins : gestion globale (tous les médecins)
- Médecins              : accès en lecture à leur propre calendrier

Routes prévues (à implémenter) :
  GET      /rendez-vous/            → liste / calendrier
  GET/POST /rendez-vous/nouveau     → prendre un rendez-vous
  GET      /rendez-vous/<id>        → détail
  GET/POST /rendez-vous/<id>/edit   → modifier
  POST     /rendez-vous/<id>/annuler → annuler
"""

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.utils.decorators import role_required

rendez_vous_bp = Blueprint('rendez_vous', __name__)


# ---------------------------------------------------------------------------
# Calendrier / liste des rendez-vous
# ---------------------------------------------------------------------------

@rendez_vous_bp.route('/')
@login_required
@role_required('secretaire', 'admin', 'medecin')
def index():
    """
    Affiche les rendez-vous :
      - Médecin    → uniquement les siens
      - Secrétaire → tous les rendez-vous
    """
    from app.models.rendez_vous import RendezVous
    from app.models.medecin     import Medecin

    if current_user.role == 'medecin':
        # Récupérer la fiche médecin liée au compte connecté
        medecin = Medecin.query.filter_by(user_id=current_user.id).first_or_404()
        rdvs = (RendezVous.query
                .filter_by(medecin_id=medecin.id)
                .order_by(RendezVous.date, RendezVous.heure)
                .all())
    else:
        rdvs = RendezVous.query.order_by(RendezVous.date, RendezVous.heure).all()

    return render_template('rendez_vous/index.html', rendez_vous=rdvs)
