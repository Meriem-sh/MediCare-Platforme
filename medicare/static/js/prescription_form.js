document.addEventListener("DOMContentLoaded", () => {
    const card = document.querySelector(".prescription-card");
    if (card) {
        // Soft fade-in animation
        card.style.opacity = 0;
        card.style.transform = "translateY(10px)";
        requestAnimationFrame(() => {
            card.style.transition = "opacity 0.4s ease, transform 0.4s ease";
            card.style.opacity = 1;
            card.style.transform = "translateY(0)";
        });
    }

    // Highlight card border when form has unsaved changes
    const form = document.querySelector(".prescription-form");
    if (form && card) {
        let dirty = false;
        form.addEventListener("change", () => {
            if (!dirty) {
                dirty = true;
                card.style.boxShadow = "0 0 0 2px rgba(14,165,233,0.5), 0 10px 35px rgba(15,23,42,0.2)";
            }
        });
    }
});
