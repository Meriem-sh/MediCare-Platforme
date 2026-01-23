from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from prescriptions.models import Prescription
from reminders.models import Reminder, DoseLog
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from .forms import PatientSignUpForm
from django.core.mail import send_mail


@login_required
def dashboard_redirect(request):
    user = request.user
    
    if user.is_superuser or user.is_staff:
        return redirect('admin:index')
    
    if user.role == 'doctor':
        return redirect('doctor_dashboard')
    elif user.role == 'patient':
        return redirect('patient_dashboard')
    else:
        return redirect('home')


@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return redirect('patient_dashboard')
    
    patients = CustomUser.objects.filter(role='patient').select_related('disease', 'assigned_doctor')
    
    rare_patients = CustomUser.objects.filter(
        role='patient',
        disease__is_rare=True
    ).select_related('disease')
    
    # ✅ FIX: Use drug__disease instead of disease
    prescriptions = Prescription.objects.filter(
        doctor=request.user
    ).select_related('patient', 'drug', 'drug__disease').order_by('-created_at')[:10]
    
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


@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':
        return redirect('doctor_dashboard')
    
    patient = request.user
    
    # ✅ FIX: Use drug__disease for proper optimization
    prescriptions = Prescription.objects.filter(
        patient=request.user
    ).select_related('doctor', 'drug', 'drug__disease').order_by('-created_at')
    
    # ✅ FIX: Use direct patient field in Reminder
    reminders = Reminder.objects.filter(
        patient=request.user,
        is_active=True
    ).select_related('prescription__drug', 'prescription__drug__disease').order_by('time')
    
    # ✅ FIX: Use direct patient field through reminder
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


@login_required
def doctor_adherence(request):
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
    
    adherence_data.sort(key=lambda x: x['adherence_percent'])
    
    context = {
        'adherence_data': adherence_data,
    }
    
    return render(request, 'users/doctor_adherence.html', context)


@require_POST
@login_required
def custom_logout(request):
    logout(request)
    return redirect('home')


@login_required
def suggest_specialists(request):
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
    
    return render(request, 'users/suggest_specialists.html', context)


@login_required
def assign_doctor(request, doctor_id):
    patient = request.user
    if patient.role != 'patient':
        return redirect('doctor_dashboard')
    
    doctor = get_object_or_404(CustomUser, id=doctor_id, role='doctor')
    patient.assigned_doctor = doctor
    patient.save()
    
    return redirect('patient_dashboard')


def home(request):
    return render(request, 'users/home.html')


def signup_view(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
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
