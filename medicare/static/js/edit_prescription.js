document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("edit-form");
    const saveBtn = document.querySelector(".save-btn");

    if (!form || !saveBtn) return;

    // Disable button after first submit to avoid double submit
    form.addEventListener("submit", () => {
        saveBtn.disabled = true;
        saveBtn.textContent = "Saving...";
    });

    // Small focus effect on fields
    const inputs = document.querySelectorAll(".form-fields input, .form-fields select, .form-fields textarea");
    inputs.forEach(input => {
        input.addEventListener("focus", () => {
            input.style.boxShadow = "0 0 6px rgba(37,99,235,0.35)";
        });
        input.addEventListener("blur", () => {
            input.style.boxShadow = "none";
        });
    });
});
