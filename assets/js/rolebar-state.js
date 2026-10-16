/*!
 * MedicalNet — role-bar state (applied synchronously, before first paint).
 * External file (CSP: script-src 'self'). Keeps the collapsible role bar
 * closed across pages when the user dismissed it, without a visible flash.
 */
(function () {
  'use strict';
  try {
    if (window.localStorage.getItem('mn-rolebar') === 'closed') {
      document.documentElement.classList.add('rolebar-closed');
    }
  } catch (err) { /* storage unavailable — bar simply stays open */ }
})();
