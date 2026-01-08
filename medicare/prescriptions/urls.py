from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_prescription, name='create_prescription'),
    path('<int:pk>/edit/', views.edit_prescription, name='edit_prescription'),
    path('<int:pk>/delete/', views.delete_prescription, name='delete_prescription'),
]
