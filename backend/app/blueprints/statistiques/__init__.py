"""
Blueprint Statistiques
=====================
Tableau de bord statistiques pour secrétaires et admins.

Affiche :
  - RDV par mois (graphique barres)
  - Consultations par médecin (graphique camembert)
  - Consultations par spécialité (graphique camembert)
  - Taux d'annulation et de réalisation
  - Tableau récapitulatif

Routes :
  GET /statistiques/  → dashboard avec données agrégées
"""

from datetime import datetime
from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy import func, and_, literal

from app.extensions import db
from app.models.consultation import Consultation
from app.models.rendez_vous import RendezVous
from app.models.medecin import Medecin
from app.models.patient import Patient
from app.utils.decorators import role_required

statistiques_bp = Blueprint('statistiques', __name__)


@statistiques_bp.route('/')
@login_required
@role_required('secretaire', 'admin')
def index():
    """Affiche le tableau de bord statistiques avec graphiques et données agrégées."""

    # Récupérer les paramètres de filtrage
    annee = request.args.get('annee', datetime.now().year, type=int)
    mois_debut = request.args.get('mois_debut', 1, type=int)
    mois_fin = request.args.get('mois_fin', 12, type=int)

    # Filtrer les rendez-vous par année et plage de mois
    rdv_query = RendezVous.query.filter(
        and_(
            func.strftime('%Y', RendezVous.date) == str(annee),
            func.strftime('%m', RendezVous.date) >= str(mois_debut).zfill(2),
            func.strftime('%m', RendezVous.date) <= str(mois_fin).zfill(2),
        )
    )

    # ─── RDV par mois (graphique barres) ───────────────────────────────────
    rdv_par_mois_raw = db.session.query(
        func.strftime('%m', RendezVous.date).label('mois'),
        func.count(RendezVous.id).label('total'),
    ).filter(
        func.strftime('%Y', RendezVous.date) == str(annee)
    ).group_by('mois').order_by('mois').all()

    # Remplir les mois manquants avec 0
    mois_labels = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun',
                   'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
    rdv_counts = [0] * 12
    for mois_str, count in rdv_par_mois_raw:
        mois_idx = int(mois_str) - 1
        rdv_counts[mois_idx] = count

    # ─── Consultations par médecin (graphique camembert) ────────────────────
    date_filters = and_(
        func.strftime('%Y', RendezVous.date) == str(annee),
        func.strftime('%m', RendezVous.date) >= str(mois_debut).zfill(2),
        func.strftime('%m', RendezVous.date) <= str(mois_fin).zfill(2),
    )

    cons_par_medecin_raw = db.session.query(
        Medecin.id,
        Medecin.nom,
        Medecin.prenom,
        Medecin.specialite,
        func.count(Consultation.id).label('nb_consultations'),
    ).join(
        RendezVous, RendezVous.medecin_id == Medecin.id
    ).join(
        Consultation, Consultation.rendez_vous_id == RendezVous.id
    ).filter(date_filters
    ).group_by(Medecin.id, Medecin.nom, Medecin.prenom, Medecin.specialite
    ).order_by(func.count(Consultation.id).desc()).all()

    medecins_labels = [f"{m.prenom} {m.nom}" for m in cons_par_medecin_raw]
    medecins_data = [m.nb_consultations for m in cons_par_medecin_raw]

    # ─── Consultations par spécialité (graphique camembert) ─────────────────
    cons_par_specialite_raw = db.session.query(
        Medecin.specialite,
        func.count(Consultation.id).label('nb_consultations'),
    ).join(
        RendezVous, RendezVous.medecin_id == Medecin.id
    ).join(
        Consultation, Consultation.rendez_vous_id == RendezVous.id
    ).filter(date_filters
    ).group_by(Medecin.specialite
    ).order_by(func.count(Consultation.id).desc()).all()

    specialites_labels = [s.specialite for s in cons_par_specialite_raw]
    specialites_data = [s.nb_consultations for s in cons_par_specialite_raw]

    # ─── Statistiques globales ─────────────────────────────────────────────
    total_rdv = rdv_query.count()
    rdv_effectues = rdv_query.filter(RendezVous.statut == 'effectue').count()
    rdv_annules = rdv_query.filter(RendezVous.statut == 'annule').count()
    rdv_programmes = rdv_query.filter(RendezVous.statut == 'programme').count()

    taux_realisation = (rdv_effectues / total_rdv * 100) if total_rdv > 0 else 0
    taux_annulation = (rdv_annules / total_rdv * 100) if total_rdv > 0 else 0

    # ─── Tableau détaillé : Médecins avec statistiques ─────────────────────
    medecins_stats = []
    for med in cons_par_medecin_raw:
        nb_rdv = db.session.query(func.count(RendezVous.id)).filter(
            RendezVous.medecin_id == med.id,
            func.strftime('%Y', RendezVous.date) == str(annee),
        ).scalar()

        medecins_stats.append({
            'nom': f"{med.prenom} {med.nom}",
            'specialite': med.specialite,
            'nb_consultations': med.nb_consultations,
            'nb_rdv': nb_rdv or 0,
            'taux': (med.nb_consultations / nb_rdv * 100) if (nb_rdv or 0) > 0 else 0,
        })

    # ─── Années disponibles pour le sélecteur ──────────────────────────────
    annees_disponibles = db.session.query(
        func.strftime('%Y', RendezVous.date).label('annee')
    ).distinct().order_by('annee').all()
    annees = [int(a.annee) for a in annees_disponibles] if annees_disponibles else [datetime.now().year]

    # Retourner le template avec toutes les données
    return render_template(
        'statistiques/index.html',
        annee=annee,
        mois_debut=mois_debut,
        mois_fin=mois_fin,
        annees=annees,
        # Statistiques globales
        total_rdv=total_rdv,
        rdv_effectues=rdv_effectues,
        rdv_annules=rdv_annules,
        rdv_programmes=rdv_programmes,
        taux_realisation=round(taux_realisation, 1),
        taux_annulation=round(taux_annulation, 1),
        # Graphiques
        mois_labels=mois_labels,
        rdv_counts=rdv_counts,
        medecins_labels=medecins_labels,
        medecins_data=medecins_data,
        specialites_labels=specialites_labels,
        specialites_data=specialites_data,
        # Tableau détaillé
        medecins_stats=medecins_stats,
    )
