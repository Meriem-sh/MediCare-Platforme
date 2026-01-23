document.addEventListener("DOMContentLoaded", () => {
    // Fade-in animation for cards
    const cards = document.querySelectorAll(".card");
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.transition = "opacity 0.4s ease, transform 0.4s ease";
            card.style.opacity = 1;
            card.style.transform = "translateY(0)";
        }, 80 * index);
    });

    // Color-code dose history status
    const historyItems = document.querySelectorAll(".history-item");
    historyItems.forEach(item => {
        const status = (item.dataset.status || "").toLowerCase();
        if (status.includes("taken")) {
            item.classList.add("status-taken");
        } else if (status.includes("missed")) {
            item.classList.add("status-missed");
        }
    });
    
    // Add Quick Actions
    addQuickActionsToPatient();
});

function addQuickActionsToPatient() {
    const mainContainer = document.querySelector('.patient-page');
    
    if (mainContainer && !document.querySelector('.quick-actions-section')) {
        const quickActionsHTML = `
            <section class="card mt-4">
                <div class="card-header">
                    <h2>⚡ Quick Actions</h2>
                </div>
                <div class="quick-actions-grid">
                    <a href="/users/specialists/" class="quick-action-btn">
                        <i class="fas fa-user-md"></i>
                        <span>Find Specialist</span>
                    </a>
                    <a href="/users/patient/dashboard/" class="quick-action-btn">
                        <i class="fas fa-sync-alt"></i>
                        <span>Refresh Dashboard</span>
                    </a>
                    <a href="/" class="quick-action-btn">
                        <i class="fas fa-home"></i>
                        <span>Go to Home</span>
                    </a>
                </div>
            </section>
        `;
        
        mainContainer.insertAdjacentHTML('beforeend', quickActionsHTML);
    }
}
