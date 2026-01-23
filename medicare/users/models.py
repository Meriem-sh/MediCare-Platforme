# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from drugs.models import Disease



class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    
    SPECIALTY_CHOICES = (
        ('generalist', 'Generalist'),
        ('oncologist', 'Oncologist'),
        ('cardiologist', 'Cardiologist'),
        ('pediatrician', 'Pediatrician'),
        ('neurologist', 'Neurologist'),
        ('endocrinologist', 'Endocrinologist'),
        ('pulmonologist', 'Pulmonologist'),
        ('other', 'Other'),
    )


    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    condition = models.CharField(max_length=255, blank=True, null=True)  # for patients only
    
    disease = models.ForeignKey(
        Disease,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='patients'
    )
    
    specialty = models.CharField(
        max_length=50,
        choices=SPECIALTY_CHOICES,
        blank=True,
        null=True
    )
    
    assigned_doctor = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='patients_assigned',
        limit_choices_to={'role': 'doctor'}
    )


    def __str__(self):
        return f"{self.username} ({self.role})"
    
    @property
    def is_doctor(self):
        return self.role == 'doctor'
    
    @property
    def is_patient(self):
        return self.role == 'patient'
