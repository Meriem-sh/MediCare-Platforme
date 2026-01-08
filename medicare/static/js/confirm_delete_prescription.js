document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("delete-form");
    const deleteBtn = document.querySelector(".delete-btn");

    if (!form || !deleteBtn) return;

    form.addEventListener("submit", (event) => {
        // Extra safety confirmation
        const sure = confirm(
            "Are you sure you want to delete this prescription? This action cannot be undone."
        );
        if (!sure) {
            event.preventDefault();
            return;
        }

        // Avoid double submissions
        deleteBtn.disabled = true;
        deleteBtn.textContent = "Deleting...";
    });
});
