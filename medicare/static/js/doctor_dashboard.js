// Small animation effect on hover
document.querySelectorAll(".card").forEach(card => {
    card.addEventListener("mouseenter", () => {
        card.style.transform = "scale(1.01)";
        card.style.transition = "0.2s ease";
    });

    card.addEventListener("mouseleave", () => {
        card.style.transform = "scale(1)";
    });
});

// Add Quick Actions automatically
document.addEventListener("DOMContentLoaded", () => {
    addQuickActionsToDoctor();
});

function addQuickActionsToDoctor() {
    const mainContainer = document.querySelector('.dashboard-container');
    
    if (mainContainer && !document.querySelector('.quick-actions-section')) {
        const quickActionsHTML = `
            <section class="card mt-4">
                <h2 class="card-title">⚡ Quick Actions</h2>
                <div class="quick-actions-grid">
                    <a href="/prescriptions/create/" class="quick-action-btn">
                        <i class="fas fa-plus-circle"></i>
                        <span>New Prescription</span>
                    </a>
                    <a href="/users/doctor/adherence/" class="quick-action-btn">
                        <i class="fas fa-chart-line"></i>
                        <span>View Adherence</span>
                    </a>
                    <a href="/users/doctor/dashboard/" class="quick-action-btn">
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
