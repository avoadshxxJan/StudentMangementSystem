/**
 * EduTrack - Shared Client-Side Interactions
 * Phase 1 Foundation: Lightweight vanilla JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
    // Automatically auto-dismiss standard alert notifications after 6 seconds
    const alerts = document.querySelectorAll('.edutrack-alert');
    alerts.forEach(function (alertElement) {
        setTimeout(function () {
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alertElement);
                if (bsAlert) {
                    bsAlert.close();
                }
            }
        }, 6000);
    });
});
