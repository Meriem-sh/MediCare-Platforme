from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "drug", "dosage", "frequency", "start_date", "end_date")
    list_filter = ("doctor", "patient", "drug")
    search_fields = ("patient__username", "doctor__username", "drug__name")
    show_facets = admin.ShowFacets.ALWAYS