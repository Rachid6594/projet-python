/**
 * HopiGest - Scripts utilitaires
 */

document.addEventListener('DOMContentLoaded', function () {

  /* -------------------------------------------------------
     Sidebar toggle (mobile)
  ------------------------------------------------------- */
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.querySelector('.sidebar-overlay');

  window.toggleSidebar = function () {
    if (!sidebar) return;
    sidebar.classList.toggle('open');
    if (overlay) overlay.classList.toggle('active');
  };

  if (overlay) {
    overlay.addEventListener('click', function () {
      sidebar.classList.remove('open');
      overlay.classList.remove('active');
    });
  }

  /* -------------------------------------------------------
     Auto-dismiss flash messages (sauf danger/warning)
  ------------------------------------------------------- */
  document.querySelectorAll('.alert:not(.alert-danger):not(.alert-warning)').forEach(function (el) {
    setTimeout(function () {
      try { new bootstrap.Alert(el).close(); } catch (_) { el.remove(); }
    }, 5000);
  });

  /* -------------------------------------------------------
     Confirmation pour actions destructrices
  ------------------------------------------------------- */
  document.querySelectorAll('[data-confirm]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (!confirm(this.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });

  /* -------------------------------------------------------
     Marquer le lien actif dans la sidebar
  ------------------------------------------------------- */
  var currentPath = window.location.pathname;
  document.querySelectorAll('.sidebar-nav .nav-link').forEach(function (link) {
    var href = link.getAttribute('href');
    if (href && href !== '/' && currentPath.startsWith(href)) {
      link.classList.add('active');
    }
  });

  /* -------------------------------------------------------
     Tooltips Bootstrap (si presents)
  ------------------------------------------------------- */
  var tooltipEls = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipEls.forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

});

/* -------------------------------------------------------
   Scroll vers les erreurs de formulaire
------------------------------------------------------- */
function markFormErrors() {
  var el = document.querySelector('.form-control.is-invalid, .form-select.is-invalid');
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
}
