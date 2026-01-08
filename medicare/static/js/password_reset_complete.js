document.addEventListener("DOMContentLoaded", () => {
    const countdownEl = document.getElementById("countdown");
    const loginBtn = document.getElementById("login-btn");

    if (!countdownEl || !loginBtn) return;

    let seconds = parseInt(countdownEl.textContent, 10);
    if (Number.isNaN(seconds)) seconds = 7;

    const timer = setInterval(() => {
        seconds -= 1;
        countdownEl.textContent = seconds;

        if (seconds <= 0) {
            clearInterval(timer);
            window.location.href = loginBtn.href;
        }
    }, 1000);
});
