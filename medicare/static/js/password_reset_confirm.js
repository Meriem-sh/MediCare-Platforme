document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const button = document.getElementById("submit-btn");

    if (!form || !button) return;

    form.addEventListener("submit", () => {
        button.disabled = true;
        button.textContent = "Validation...";
    });
});
