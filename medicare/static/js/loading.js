// Loading Spinner Management
document.addEventListener('DOMContentLoaded', function() {
    // Create loading overlay if it doesn't exist
    if (!document.getElementById('loadingOverlay')) {
        const overlay = document.createElement('div');
        overlay.id = 'loadingOverlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div>
                <div class="spinner"></div>
                <div class="loading-text">Loading...</div>
            </div>
        `;
        document.body.insertBefore(overlay, document.body.firstChild);
    }
    
    // Hide loading spinner when page is fully loaded
    window.addEventListener('load', hideLoadingSpinner);
    
    // Show loading spinner on navigation
    setupNavigationListeners();
    
    // Show spinner on form submission
    setupFormListeners();
});

function hideLoadingSpinner() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.add('hidden');
        setTimeout(() => {
            overlay.style.display = 'none';
        }, 300);
    }
}

function showLoadingSpinner() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'flex';
        overlay.classList.remove('hidden');
    }
}

function setupNavigationListeners() {
    const links = document.querySelectorAll('a:not([target="_blank"]):not([href^="#"]):not([href^="javascript:"])');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.href && this.href !== 'javascript:void(0)' && this.href !== '#') {
                showLoadingSpinner();
            }
        });
    });
}

function setupFormListeners() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Don't show spinner for AJAX forms
            if (!form.classList.contains('ajax-form')) {
                showLoadingSpinner();
            }
        });
    });
}

// Hide spinner on browser back button
window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        hideLoadingSpinner();
    }
});
