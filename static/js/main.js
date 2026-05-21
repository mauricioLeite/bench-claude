/* DevConnect - Main JS utilities */

(function () {
  'use strict';

  // Auto-dismiss alerts after 4 seconds
  function initAutoDismissAlerts() {
    var alerts = document.querySelectorAll('.alert.auto-dismiss');
    alerts.forEach(function (alert) {
      setTimeout(function () {
        var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
      }, 4000);
    });
  }

  // Activate current nav link based on URL
  function highlightActiveNav() {
    var currentPath = window.location.pathname;
    var navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(function (link) {
      var href = link.getAttribute('href');
      if (href && href !== '/' && currentPath.startsWith(href)) {
        link.classList.add('active');
      } else if (href === '/' && currentPath === '/') {
        link.classList.add('active');
      }
    });
  }

  // Confirm before form submissions that have data-confirm attribute
  function initConfirmForms() {
    var forms = document.querySelectorAll('form[data-confirm]');
    forms.forEach(function (form) {
      form.addEventListener('submit', function (e) {
        var msg = form.getAttribute('data-confirm');
        if (!window.confirm(msg)) {
          e.preventDefault();
        }
      });
    });
  }

  // Show character count for textareas with data-maxlength
  function initCharCounters() {
    var textareas = document.querySelectorAll('textarea[data-maxlength]');
    textareas.forEach(function (ta) {
      var max = parseInt(ta.getAttribute('data-maxlength'));
      var counter = document.createElement('div');
      counter.className = 'form-text text-end';
      counter.textContent = ta.value.length + ' / ' + max;
      ta.parentNode.insertBefore(counter, ta.nextSibling);

      ta.addEventListener('input', function () {
        var len = ta.value.length;
        counter.textContent = len + ' / ' + max;
        if (len > max * 0.9) {
          counter.className = 'form-text text-end text-warning';
        } else {
          counter.className = 'form-text text-end';
        }
      });
    });
  }

  // Initialize tooltips
  function initTooltips() {
    var tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(function (el) {
      new bootstrap.Tooltip(el);
    });
  }

  // Run on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', function () {
    initAutoDismissAlerts();
    highlightActiveNav();
    initConfirmForms();
    initCharCounters();
    initTooltips();
  });
})();
