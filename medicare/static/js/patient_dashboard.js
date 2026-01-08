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
});
