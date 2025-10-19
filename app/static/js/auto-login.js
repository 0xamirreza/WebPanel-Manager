// Auto-login functionality for WebPanel Manager

// Auto-submit the form after a short delay
setTimeout(function() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.submit();
    }
}, 2000);

// Fallback: if form doesn't submit, show manual login option
setTimeout(function() {
    const cardBody = document.querySelector('.card-body');
    if (cardBody) {
        // Get panel data from the template (these variables should be available globally)
        const panelLoginUrl = window.panelLoginUrl || '';
        const panelUsername = window.panelUsername || '';
        const panelPassword = window.panelPassword || '';
        
        cardBody.innerHTML = `
            <div class="mb-4">
                <i class="bi bi-exclamation-triangle text-warning" style="font-size: 3rem;"></i>
            </div>
            <h5>Manual Login Required</h5>
            <p class="text-muted">Auto-login failed. Please click the button below to open the panel manually.</p>
            <a href="${panelLoginUrl}" target="_blank" class="btn btn-primary">
                <i class="bi bi-box-arrow-in-right"></i> Open Panel
            </a>
            <br><br>
            <small class="text-muted">
                Username: ${panelUsername}<br>
                Password: ${panelPassword}
            </small>
        `;
    }
}, 10000);
