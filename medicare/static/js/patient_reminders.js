document.addEventListener("DOMContentLoaded", () => {

    // Ask for browser notification permission once
    if ("Notification" in window && Notification.permission === "default") {
        Notification.requestPermission();
    }

    // Function to show in-page popup
    function showInPageReminder(reminder) {
        let container = document.querySelector(".reminder-popup-container");
        if (!container) {
            container = document.createElement("div");
            container.className = "reminder-popup-container";
            document.body.appendChild(container);
        }

        const box = document.createElement("div");
        box.className = "reminder-popup";

        box.innerHTML = `
            <h4>Medication Reminder</h4>
            <p><strong>Drug:</strong> ${reminder.drug || "Your medication"}</p>
            ${reminder.dosage ? `<p><strong>Dosage:</strong> ${reminder.dosage}</p>` : ""}
            ${reminder.frequency ? `<p><strong>Frequency:</strong> ${reminder.frequency}</p>` : ""}
            <p>${reminder.message || "It is time to take your medication."}</p>
            <button class="reminder-close-btn">OK</button>
        `;

        container.appendChild(box);

        box.querySelector(".reminder-close-btn").addEventListener("click", () => {
            box.remove();
        });
    }

    // Function to send browser notification
    function showBrowserNotification(reminder) {
        if (!("Notification" in window)) {
            return;
        }
        if (Notification.permission !== "granted") {
            return;
        }

        const title = "Medication Reminder";
        const bodyParts = [];
        if (reminder.drug) bodyParts.push(`Drug: ${reminder.drug}`);
        if (reminder.dosage) bodyParts.push(`Dosage: ${reminder.dosage}`);
        bodyParts.push(reminder.message || "It is time to take your medication.");

        const body = bodyParts.join("\n");

        new Notification(title, { body: body });
    }

    // Polling function
    function checkDueReminders() {
        fetch("/reminders/api/due/")
            .then(response => response.json())
            .then(data => {
                if (!data.reminders || !data.reminders.length) return;
                data.reminders.forEach(reminder => {
                    showInPageReminder(reminder);
                    showBrowserNotification(reminder);
                });
            })
            .catch(err => {
                console.error("Error fetching reminders:", err);
            });
    }

    // First check immediately, then every 60 seconds
    checkDueReminders();
    setInterval(checkDueReminders, 60 * 1000);
});
