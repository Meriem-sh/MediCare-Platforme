document.addEventListener("DOMContentLoaded", () => {
    const fills = document.querySelectorAll(".adherence-bar-fill");

    fills.forEach(fill => {
        const percentRaw = fill.dataset.percent || "0";
        let percent = parseFloat(percentRaw);

        if (isNaN(percent)) percent = 0;
        percent = Math.max(0, Math.min(percent, 100)); // clamp 0–100

        // Color category
        if (percent < 80) {
            fill.classList.add("low");
            const row = fill.closest("tr");
            if (row) row.classList.add("adherence-low-row");
        } else if (percent < 95) {
            fill.classList.add("medium");
        } else {
            // default (green) = high
        }

        // Animate width after a tiny delay
        requestAnimationFrame(() => {
            fill.style.width = percent + "%";
        });
    });
    
    // Add Back Button
    addBackButtonToAdherence();
});

function addBackButtonToAdherence() {
    const adherenceHeader = document.querySelector('.adherence-header');
    
    if (adherenceHeader && !document.querySelector('.back-btn-container')) {
        const backButtonHTML = `
            <div class="back-btn-container">
                <a href="/users/doctor/dashboard/" class="btn btn-secondary back-btn">
                    <i class="fas fa-arrow-left"></i> Back to Dashboard
                </a>
            </div>
        `;
        
        adherenceHeader.insertAdjacentHTML('beforeend', backButtonHTML);
    }
}
