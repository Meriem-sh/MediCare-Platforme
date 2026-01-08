document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const button = document.getElementById("submit-btn");

    form.addEventListener("submit", () => {
        button.disabled = true;
        button.textContent = "Envoi en cours...";
    });
});
