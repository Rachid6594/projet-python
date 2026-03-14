/**
 * HôpiGest - Scripts utilitaires
 */

document.addEventListener('DOMContentLoaded', function() {
    // Fermer automatiquement les alertes après 5 secondes
    const alerts = document.querySelectorAll('.alert:not(.alert-danger):not(.alert-warning)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirmation pour les actions destructrices
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });
});

// Fonction d'aide pour afficher les erreurs de formulaire
function markFormErrors() {
    const inputs = document.querySelectorAll('.form-control.is-invalid, .form-select.is-invalid');
    inputs.forEach(input => {
        input.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
}
