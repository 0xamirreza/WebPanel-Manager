// Dashboard functionality for WebPanel Manager

// Show restore modal based on type
function showRestoreModal(type) {
    if (type === 'json') {
        const modal = new bootstrap.Modal(document.getElementById('jsonRestoreModal'));
        modal.show();
    } else if (type === 'database') {
        const modal = new bootstrap.Modal(document.getElementById('databaseRestoreModal'));
        modal.show();
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Any dashboard-specific initialization can go here
    console.log('Dashboard loaded');
});
