document.addEventListener("DOMContentLoaded", () => {

    // Toggle password visibility
    const pwFields = document.querySelectorAll("input[type='password']");
    pwFields.forEach(field => {
        const toggleBtn = document.createElement("span");
        toggleBtn.classList.add("toggle-password");
        toggleBtn.innerText = "👁️";
        toggleBtn.style.cursor = "pointer";
        toggleBtn.style.marginLeft = "-25px";
        toggleBtn.style.userSelect = "none";

        field.parentNode.appendChild(toggleBtn);

        toggleBtn.addEventListener("click", () => {
            field.type = field.type === "password" ? "text" : "password";
        });
    });

    // Input highlight effect
    const inputs = document.querySelectorAll(".auth-form input, .auth-form textarea, .auth-form select");
    inputs.forEach(input => {
        input.addEventListener("focus", () => {
            input.style.boxShadow = "0 0 6px rgba(37,99,235,0.35)";
        });
        input.addEventListener("blur", () => {
            input.style.boxShadow = "none";
        });
    });

});
