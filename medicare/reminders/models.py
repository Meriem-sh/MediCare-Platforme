from django.db import models

# Create your models here.
from django.conf import settings
from prescriptions.models import Prescription

class Reminder(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='reminders'
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'}
    )
    time = models.TimeField()  # e.g. 08:00, 14:00
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for {self.patient} at {self.time}"

#optional but useful for tracking taken/missed
class DoseLog(models.Model):
    STATUS_CHOICES = (
        ('taken', 'Taken'),
        ('missed', 'Missed'),
    )

    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE, related_name='dose_logs')
    scheduled_for = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    logged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reminder.patient} - {self.status} ({self.scheduled_for})"
