// Web Panel Manager JavaScript

// Note: panelData is initialized in the HTML template
// This file contains all the functionality that uses the global panelData variable

// Delete confirmation modal
function confirmDelete(panelId, panelName) {
    document.getElementById('panelName').textContent = panelName;
    document.getElementById('deleteForm').action = `/panels/delete/${panelId}`;
    
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}

// Show panel info modal
function showPanelInfo(panelId) {
    const panel = panelData[panelId];
    if (!panel) return;
    
    const modalBody = document.getElementById('infoModalBody');
    modalBody.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <h6><i class="bi bi-tag me-2"></i>Basic Information</h6>
                <table class="table table-sm">
                    <tr><td><strong>Name:</strong></td><td>${panel.name}</td></tr>
                    <tr><td><strong>Domain:</strong></td><td>${panel.domain}</td></tr>
                    <tr><td><strong>Panel Type:</strong></td><td><span class="badge bg-secondary">${panel.panel_type.toUpperCase()}</span></td></tr>
                    <tr><td><strong>Provider:</strong></td><td>${panel.host_provider || 'Not specified'}</td></tr>
                    <tr><td><strong>Created:</strong></td><td>${panel.created_at}</td></tr>
                </table>
            </div>
            <div class="col-md-6">
                <h6><i class="bi bi-key me-2"></i>Login Information</h6>
                <table class="table table-sm">
                    <tr><td><strong>Login URL:</strong></td><td><a href="${panel.login_url}" target="_blank" class="text-decoration-none">${panel.login_url}</a></td></tr>
                    <tr><td><strong>Username:</strong></td><td><span class="copyable-text" data-value="${panel.username}">${panel.username} <i class="fas fa-copy ms-1 copy-icon" title="Copy username"></i></span></td></tr>
                    <tr><td><strong>Password:</strong></td><td><span class="password-container" data-value="${panel.password}"><span class="password-text">••••••••</span> <i class="fas fa-eye ms-1 password-toggle" title="Show password"></i> <i class="fas fa-copy ms-1 copy-icon" title="Copy password"></i></span></td></tr>
                </table>
            </div>
        </div>
        ${panel.notes ? `
        <div class="mt-3">
            <h6><i class="bi bi-sticky me-2"></i>Notes</h6>
            <div class="alert alert-light">
                ${panel.notes.replace(/\n/g, '<br>')}
            </div>
        </div>
        ` : ''}
    `;
    
    // Re-attach copy functionality to new elements
    attachCopyFunctionality();
    
    const infoModal = new bootstrap.Modal(document.getElementById('infoModal'));
    infoModal.show();
}

// Attach copy functionality to elements
function attachCopyFunctionality() {
    const copyableElements = document.querySelectorAll('.copyable-text');
    
    copyableElements.forEach(element => {
        // Handle clicks on the text or icon
        element.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            copyToClipboard(element);
        });
        
        // Also handle direct clicks on the icon
        const icon = element.querySelector('.copy-icon');
        if (icon) {
            icon.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                copyToClipboard(element);
            });
        }
    });
    
    // Handle password containers
    const passwordContainers = document.querySelectorAll('.password-container');
    passwordContainers.forEach(container => {
        const passwordText = container.querySelector('.password-text');
        const toggleIcon = container.querySelector('.password-toggle');
        const copyIcon = container.querySelector('.copy-icon');
        const actualPassword = container.getAttribute('data-value');
        
        // Handle eye icon click (toggle visibility)
        toggleIcon.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (passwordText.textContent === '••••••••') {
                passwordText.textContent = actualPassword;
                toggleIcon.className = 'fas fa-eye-slash ms-1 password-toggle';
                toggleIcon.title = 'Hide password';
            } else {
                passwordText.textContent = '••••••••';
                toggleIcon.className = 'fas fa-eye ms-1 password-toggle';
                toggleIcon.title = 'Show password';
            }
        });
        
        // Handle copy icon click
        copyIcon.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            copyToClipboard(container);
        });
    });
}

// Copy to clipboard function
function copyToClipboard(element) {
    const value = element.getAttribute('data-value');
    
    // Try modern clipboard API first
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(value).then(function() {
            showCopySuccess(element);
        }).catch(function(err) {
            console.error('Clipboard API failed: ', err);
            fallbackCopyToClipboard(value, element);
        });
    } else {
        // Fallback for older browsers or non-secure contexts
        fallbackCopyToClipboard(value, element);
    }
}

// Fallback copy method
function fallbackCopyToClipboard(text, element) {
    // Create a temporary textarea element
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showCopySuccess(element);
        } else {
            showCopyError();
        }
    } catch (err) {
        console.error('Fallback copy failed: ', err);
        showCopyError();
    } finally {
        document.body.removeChild(textArea);
    }
}

// Show copy success feedback
function showCopySuccess(element) {
    element.classList.add('copy-success');
    
    const icon = element.querySelector('.copy-icon');
    const originalClass = icon.className;
    icon.className = 'fas fa-check ms-1 copy-icon';
    
    setTimeout(function() {
        element.classList.remove('copy-success');
        icon.className = originalClass;
    }, 1500);
}

// Show copy error feedback
function showCopyError() {
    // Show a simple alert for copy failure
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-warning alert-dismissible fade show position-fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>
        Failed to copy to clipboard. Please select and copy manually.
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(function() {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    attachCopyFunctionality();
});
