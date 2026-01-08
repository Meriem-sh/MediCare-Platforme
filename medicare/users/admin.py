from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

from django.contrib import admin
from drugs.models import Drug, Disease


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ("username", "email", "role","specialty", "disease", "is_staff", "is_active")
    list_filter = ("role","specialty","disease", "is_staff", "is_active")

    fieldsets = UserAdmin.fieldsets + (
        ("Role & medical info", {"fields": ("role","specialty", "phone", "condition", "disease")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("role", "phone", "condition")}),
    )

    search_fields = ("username", "email")
    ordering = ("username",)
    show_facets = admin.ShowFacets.ALWAYS
    
@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_rare', 'orpha_code')
    list_filter = ('is_rare',)
    search_fields = ('name', 'orpha_code')