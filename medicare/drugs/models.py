from django.db import models

# Create your models here.

class Drug(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    condition = models.CharField(max_length=100, blank=True, null=True)  # e.g. "Diabetes", "Hypertension"
    dosage_form = models.CharField(max_length=50, blank=True, null=True)  # e.g. "Tablet", "Syrup"
    strength = models.CharField(max_length=50, blank=True, null=True)     # e.g. "500 mg"
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Disease(models.Model):
    name = models.CharField(max_length=200)
    is_rare = models.BooleanField(default=False)
    orpha_code = models.CharField(max_length=20, blank=True, null=True)  # optional
    description = models.TextField(blank=True)
    
    # Which doctor specialty is recommended for this disease
    RECOMMENDED_SPECIALTY_CHOICES = (
        ('generalist', 'Generalist'),
        ('oncologist', 'Oncologist'),
        ('cardiologist', 'Cardiologist'),
        ('pediatrician', 'Pediatrician'),
        ('neurologist', 'Neurologist'),
        ('endocrinologist', 'Endocrinologist'),
        ('pulmonologist', 'Pulmonologist'),
        ('other', 'Other'),
    )

    recommended_specialty = models.CharField(
        max_length=50,
        choices=RECOMMENDED_SPECIALTY_CHOICES,
        blank=True,
        null=True,
        help_text="Specialist type usually needed for this disease."
    )

    def __str__(self):
        return self.name
