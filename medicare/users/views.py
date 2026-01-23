from django.shortcuts import render, redirect
# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from prescriptions.models import Prescription
from reminders.models import Reminder, DoseLog
from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import PatientSignUpForm
from django.core.mail import send_mail
from django.db.models import Q


# ===================================
# Dashboard Redirect based on Role
# ===================================
@login_required
def dashboard_redirect(request):
    """
    Redirect user to appropriate dashboard based on user role:
    - Admin/Superuser → Admin Panel
    - Doctor → Doctor Dashboard
    - Patient → Patient Dashboard
    """
    user = request.user
    
    # Check if user is admin/superuser
    if user.is_superuser or user.is_staff:
        return redirect('admin:index')  # ✅ Admin panel
    
    # Check user role
    if user.role == 'doctor':
        return redirect('doctor_dashboard')
    elif user.role == 'patient':
        return redirect('patient_dashboard')
    else:
        # Fallback to home page if no role defined
        return redirect('home')


@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return redirect('patient_dashboard')
    
    # Optimize queries with select_related
    patients = CustomUser.objects.filter(role='patient').select_related('disease', 'assigned_doctor')
    
    rare_patients = CustomUser.objects.filter(
        role='patient',
        disease__is_rare=True
    ).select_related('disease')
    
    prescriptions = Prescription.objects.filter(
        doctor=request.user
    ).select_related('patient', 'drug', 'disease').order_by('-created_at')[:10]
    
    reminders = Reminder.objects.filter(
        prescription__doctor=request.user
    ).select_related('prescription__patient', 'prescription__drug').order_by('-created_at')[:10]
    
    context = {
        'patients': patients,
        'prescriptions': prescriptions,
        'reminders': reminders,
        'rare_patients': rare_patients,
        'total_patients': patients.count(),
        'total_prescriptions': prescriptions.count(),
    }
    
    return render(request, 'users/doctor_dashboard.html', context)


@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':
        return redirect('doctor_dashboard')
    
    patient = request.user  # current logged-in patient
    
    # ✅ FIX: Optimize queries with select_related and prefetch_related
    prescriptions = Prescription.objects.filter(
        patient=request.user
    ).select_related('doctor', 'drug', 'disease').order_by('-created_at')
    
    reminders = Reminder.objects.filter(
        prescription__patient=request.user,  # ✅ FIXED
        is_active=True
    ).select_related('prescription__drug').order_by('time')
    
    # ✅ FIX: Correct the filter path
    dose_logs = DoseLog.objects.filter(
        reminder__prescription__patient=request.user  # ✅ FIXED
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


@login_required
def doctor_adherence(request):
    if request.user.role != 'doctor':
        return redirect('patient_dashboard')
    
    patients = CustomUser.objects.filter(role='patient').select_related('disease')
    adherence_data = []
    
    for patient in patients:
        logs = DoseLog.objects.filter(
            reminder__prescription__patient=patient,  # ✅ FIXED
            reminder__prescription__doctor=request.user
        )
        
        total = logs.count()
        if total == 0:
            continue  # skip patients with no logs
        
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
    
    # Sort by adherence (lowest first to highlight problems)
    adherence_data.sort(key=lambda x: x['adherence_percent'])
    
    context = {
        'adherence_data': adherence_data,
    }
    
    return render(request, 'users/doctor_adherence.html', context)


@require_POST
@login_required
def custom_logout(request):
    logout(request)
    return redirect('home')  # ✅ Updated to redirect to home


@login_required
def suggest_specialists(request):
    user = request.user
    
    # Only patients should use this
    if user.role != 'patient':
        return redirect('doctor_dashboard')  # or wherever you want
    
    # Patient must have a disease selected
    if not user.disease:
        # you can show a message instead if you use messages framework
        return render(request, 'users/no_disease_selected.html')
    
    disease = user.disease
    recommended_specialty = disease.recommended_specialty
    
    # If no specialty defined for that disease
    if not recommended_specialty:
        doctors = CustomUser.objects.filter(role='doctor').select_related('specialty')
    else:
        doctors = CustomUser.objects.filter(
            role='doctor',
            specialty=recommended_specialty
        ).select_related('specialty')
    
    context = {
        'patient': user,
        'disease': disease,
        'recommended_specialty': recommended_specialty,
        'doctors': doctors,
    }
    
    return render(request, 'users/suggest_specialists.html', context)


@login_required
def assign_doctor(request, doctor_id):
    patient = request.user
    if patient.role != 'patient':
        return redirect('doctor_dashboard')
    
    doctor = get_object_or_404(CustomUser, id=doctor_id, role='doctor')
    patient.assigned_doctor = doctor
    patient.save()
    
    return redirect('patient_dashboard')  # or a success page


def home(request):
    return render(request, 'users/home.html')


def signup_view(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # 📨 Send welcome email
            if user.email:  # only if they gave an email
                send_mail(
                    subject='Welcome to Medicare',
                    message=(
                        f'Hello {user.username},\n\n'
                        'Your patient account has been successfully created on the Medicare platform.\n'
                        'You can now log in, manage your treatments and '
                        'find specialists suitable for your disease.\n\n'
                        'This is an automated message, please do not reply.'
                    ),
                    from_email=None,  # uses DEFAULT_FROM_EMAIL
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            
            login(request, user)
            return redirect('dashboard_redirect')  # will send patient to patient_dashboard
    else:
        form = PatientSignUpForm()
    
    return render(request, 'users/signup.html', {'form': form})
