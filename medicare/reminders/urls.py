from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:prescription_id>/', views.create_reminder, name='create_reminder'),
    path('dose/<int:reminder_id>/taken/', views.mark_dose_taken, name='mark_dose_taken'),
    path('dose/<int:reminder_id>/missed/', views.mark_dose_missed, name='mark_dose_missed'),
    path('<int:pk>/edit/', views.edit_reminder, name='edit_reminder'),
    path('<int:pk>/delete/', views.delete_reminder, name='delete_reminder'),
    path('<int:reminder_id>/email/', views.email_reminder, name='email_reminder'),
    path('api/due/', views.due_reminders, name='due_reminders'),  #the endpoint : /reminders/api/due/
]
