# ---------------------------------------------------------------------------
# Registre des modèles SQLAlchemy
# ---------------------------------------------------------------------------
# Tous les modèles doivent être importés ici afin qu'Alembic (Flask-Migrate)
# puisse les détecter lors de la génération des migrations.
#
# L'ordre d'import respecte les dépendances de clés étrangères :
#   Utilisateur → Medecin → RendezVous → Consultation
#   Patient     → RendezVous
# ---------------------------------------------------------------------------

from app.models.utilisateur import Utilisateur   # noqa: F401
from app.models.patient     import Patient        # noqa: F401
from app.models.medecin     import Medecin        # noqa: F401
from app.models.rendez_vous import RendezVous     # noqa: F401
from app.models.consultation import Consultation  # noqa: F401
