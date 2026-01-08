document.addEventListener("DOMContentLoaded", function () {
  // Stagger app cards animation
  const cards = document.querySelectorAll(".app-card");
  cards.forEach((card, i) => {
    card.style.animationDelay = `${i * 0.07}s`;
  });

  // Simple floating background blobs on dashboard
  const container = document.querySelector("#content-main") || document.body;
  const blobCount = 6;

  for (let i = 0; i < blobCount; i++) {
    const blob = document.createElement("div");
    blob.className = "bg-blob";
    blob.style.left = Math.random() * 100 + "%";
    blob.style.animationDelay = `${Math.random() * 10}s`;
    container.appendChild(blob);
  }
});


// Disable Django's built-in sidebar behavior
document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("nav-sidebar");
    const toggle = document.getElementById("toggle-nav-sidebar");

    if (sidebar) sidebar.style.display = "none";
    if (toggle) toggle.style.display = "none";

    document.body.classList.remove("toggle-nav-sidebar");
});
