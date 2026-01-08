from django.contrib import admin

# Register your models here.
from .models import Reminder, DoseLog

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ("patient", "prescription", "time", "is_active")
    list_filter = ("is_active", "time")
    search_fields = ("patient__username",)

@admin.register(DoseLog)
class DoseLogAdmin(admin.ModelAdmin):
    list_display = ("reminder", "status", "scheduled_for", "logged_at")
    list_filter = ("status",)
