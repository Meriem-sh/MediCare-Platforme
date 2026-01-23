from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.contrib import messages
from django import forms

from .models import CustomUser
from .forms import PatientSignUpForm
from prescriptions.models import Prescription
from reminders.models import Reminder, DoseLog


# ============================================
# HOME & AUTHENTICATION
# ============================================

def home(request):
    """Landing page"""
    return render(request, 'users/home.html')


def signup_view(request):
    """User signup with email notification"""
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Send welcome email
            if user.email:
                send_mail(
                    subject='Welcome to Medicare',
                    message=(
                        f'Hello {user.username},\n\n'
                        'Your patient account has been successfully created on the Medicare platform.\n'
                        'You can now log in, manage your treatments and '
                        'find specialists suitable for your disease.\n\n'
                        'This is an automated message, please do not reply.'
                    ),
                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            
            login(request, user)
            return redirect('dashboard_redirect')
    else:
        form = PatientSignUpForm()
    
    return render(request, 'users/signup.html', {'form': form})


@require_POST
@login_required
def custom_logout(request):
    """Custom logout view"""
    logout(request)
    return redirect('home')


# ============================================
# DASHBOARD REDIRECTS
# ============================================

@login_required
def dashboard_redirect(request):
    """Redirect users to appropriate dashboard based on role"""
    user = request.user
    
    if user.is_superuser or user.is_staff:
        return redirect('admin:index')
    
    if user.role == 'doctor':
        return redirect('doctor_dashboard')
    elif user.role == 'patient':
        return redirect('patient_dashboard')
    else:
        return redirect('home')


# ============================================
# DOCTOR DASHBOARD
# ============================================

@login_required
def doctor_dashboard(request):
    """Doctor dashboard with patients, prescriptions, and reminders"""
    if request.user.role != 'doctor':
        return redirect('patient_dashboard')
    
    # Get all patients with optimized queries
    patients = CustomUser.objects.filter(
        role='patient'
    ).select_related('disease', 'assigned_doctor')
    
    # Get rare disease patients
    rare_patients = CustomUser.objects.filter(
        role='patient',
        disease__is_rare=True
    ).select_related('disease')
    
    # Get recent prescriptions
    prescriptions = Prescription.objects.filter(
        doctor=request.user
    ).select_related('patient', 'drug').order_by('-created_at')[:10]
    
    # Get recent reminders
    reminders = Reminder.objects.filter(
        prescription__doctor=request.user
    ).select_related('patient', 'prescription__drug').order_by('-created_at')[:10]
    
    context = {
        'patients': patients,
        'prescriptions': prescriptions,
        'reminders': reminders,
        'rare_patients': rare_patients,
        'total_patients': patients.count(),
        'total_prescriptions': prescriptions.count(),
    }
    
    return render(request, 'users/doctor_dashboard.html', context)


# ============================================
# PATIENT DASHBOARD
# ============================================

@login_required
def patient_dashboard(request):
    """Patient dashboard with prescriptions, reminders, and dose logs"""
    if request.user.role != 'patient':
        return redirect('doctor_dashboard')
    
    patient = request.user
    
    # Get prescriptions (optimized)
    prescriptions = Prescription.objects.filter(
        patient=request.user
    ).select_related('doctor', 'drug').order_by('-created_at')
    
    # Get active reminders (optimized)
    reminders = Reminder.objects.filter(
        patient=request.user,
        is_active=True
    ).select_related('prescription__drug').order_by('time')
    
    # Get recent dose logs (optimized)
    dose_logs = DoseLog.objects.filter(
        reminder__patient=request.user
    ).select_related('reminder__prescription__drug').order_by('-logged_at')[:20]
    
    context = {
        'patient': patient,
        'prescriptions': prescriptions,
        'reminders': reminders,
        'dose_logs': dose_logs,
        'total_prescriptions': prescriptions.count(),
        'active_reminders': reminders.count(),
    }
    
    return render(request, 'users/patient_dashboard.html', context)


# ============================================
# DOCTOR ADHERENCE TRACKING
# ============================================

@login_required
def doctor_adherence(request):
    """Doctor view to track patient medication adherence"""
    if request.user.role != 'doctor':
        return redirect('patient_dashboard')
    
    patients = CustomUser.objects.filter(role='patient').select_related('disease')
    adherence_data = []
    
    for patient in patients:
        logs = DoseLog.objects.filter(
            reminder__patient=patient,
            reminder__prescription__doctor=request.user
        )
        
        total = logs.count()
        if total == 0:
            continue
        
        taken_count = logs.filter(status='taken').count()
        missed_count = logs.filter(status='missed').count()
        adherence_percent = round((taken_count / total) * 100, 1) if total > 0 else 0
        
        adherence_data.append({
            'patient': patient,
            'taken': taken_count,
            'missed': missed_count,
            'total': total,
            'adherence_percent': adherence_percent,
        })
    
    # Sort by adherence percentage (lowest first)
    adherence_data.sort(key=lambda x: x['adherence_percent'])
    
    context = {
        'adherence_data': adherence_data,
    }
    
    return render(request, 'users/doctor_adherence.html', context)


# ============================================
# SPECIALIST RECOMMENDATION
# ============================================

@login_required
def suggest_specialists(request):
    """Suggest specialists based on patient's disease"""
    user = request.user
    
    if user.role != 'patient':
        return redirect('doctor_dashboard')
    
    if not user.disease:
        return render(request, 'users/no_disease_selected.html')
    
    disease = user.disease
    recommended_specialty = disease.recommended_specialty
    
    if not recommended_specialty:
        doctors = CustomUser.objects.filter(role='doctor')
    else:
        doctors = CustomUser.objects.filter(
            role='doctor',
            specialty=recommended_specialty
        )
    
    context = {
        'patient': user,
        'disease': disease,
        'recommended_specialty': recommended_specialty,
        'doctors': doctors,
    }
    
    return render(request, 'users/suggest_specialist.html', context)


@login_required
def assign_doctor(request, doctor_id):
    """Assign a doctor to the current patient"""
    patient = request.user
    if patient.role != 'patient':
        return redirect('doctor_dashboard')
    
    doctor = get_object_or_404(CustomUser, id=doctor_id, role='doctor')
    patient.assigned_doctor = doctor
    patient.save()
    
    messages.success(request, f'Dr. {doctor.username} has been assigned to you successfully!')
    return redirect('patient_dashboard')


# ============================================
# PROFILE & SETTINGS
# ============================================

class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile"""
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'disease']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'disease': forms.Select(attrs={'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs.get('instance')
        # Remove disease field if user is not a patient
        if user and user.role != 'patient':
            self.fields.pop('disease', None)


@login_required
def profile_view(request):
    """View user profile"""
    return render(request, 'users/profile.html')


@login_required
def profile_edit_view(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def settings_view(request):
    """User settings page with password change"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'users/settings.html', {'form': form})
