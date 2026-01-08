from django.db import models

# Create your models here.
from django.conf import settings
from drugs.models import Drug

class Prescription(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_prescriptions',
        limit_choices_to={'role': 'doctor'}
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_prescriptions',
        limit_choices_to={'role': 'patient'}
    )
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)      # e.g. "1 tablet"
    frequency = models.CharField(max_length=100)   # e.g. "3 times a day"
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.drug} ({self.dosage})"
