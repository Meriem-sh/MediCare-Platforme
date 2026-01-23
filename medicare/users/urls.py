from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # ============================================
    # HOME PAGE
    # ============================================
    path('', views.home, name='home'),
    
    
    # ============================================
    # AUTHENTICATION
    # ============================================
    path('login/', 
         auth_views.LoginView.as_view(template_name='users/login.html'), 
         name='login'),
    
    path('signup/', 
         views.signup_view, 
         name='signup'),
    
    path('logout/', 
         views.custom_logout, 
         name='logout'),
    
    
    # ============================================
    # PASSWORD RESET
    # ============================================
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    
    
    # ============================================
    # DASHBOARDS
    # ============================================
    path('dashboard/', 
         views.dashboard_redirect, 
         name='dashboard_redirect'),
    
    path('doctor/dashboard/', 
         views.doctor_dashboard, 
         name='doctor_dashboard'),
    
    path('patient/dashboard/', 
         views.patient_dashboard, 
         name='patient_dashboard'),
    
    path('doctor/adherence/', 
         views.doctor_adherence, 
         name='doctor_adherence'),
    
    
    # ============================================
    # SPECIALIST RECOMMENDATION
    # ============================================
    path('specialists/', 
         views.suggest_specialists, 
         name='suggest_specialists'),
    
    path('assign-doctor/<int:doctor_id>/', 
         views.assign_doctor, 
         name='assign_doctor'),
    
    
    # ============================================
    # PROFILE & SETTINGS
    # ============================================
    path('profile/', 
         views.profile_view, 
         name='profile'),
    
    path('profile/edit/', 
         views.profile_edit_view, 
         name='profile_edit'),
    
    path('settings/', 
         views.settings_view, 
         name='settings'),
]
