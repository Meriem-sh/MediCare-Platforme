from django.contrib import admin

# Register your models here.
from .models import Drug

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ("name", "condition", "dosage_form", "strength", "is_active")
    list_filter = ("condition", "is_active")
    search_fields = ("name", "condition")
    show_facets = admin.ShowFacets.ALWAYS