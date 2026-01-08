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


#from login redirect (settings), till here to check roles
@login_required
def dashboard_redirect(request):
    user = request.user
    if user.role == 'doctor':
        return redirect('doctor_dashboard')
    elif user.role == 'patient':
        return redirect('patient_dashboard')
    else:
        return redirect('login')  # fallback

@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return redirect('patient_dashboard')

    patients = CustomUser.objects.filter(role='patient')
    rare_patients = CustomUser.objects.filter(
        role='patient',
        disease__is_rare=True
    ).select_related('disease')
    prescriptions = Prescription.objects.filter(doctor=request.user)
    
    reminders = Reminder.objects.filter(prescription__doctor=request.user)


    context = {
        'patients': patients,
        'prescriptions': prescriptions,
        'reminders': reminders,
        'rare_patients': rare_patients,
    }
    return render(request, 'users/doctor_dashboard.html', context)

@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':
        return redirect('doctor_dashboard')

    patient = request.user  # current logged-in patient
    prescriptions = Prescription.objects.filter(patient=request.user)
    reminders = Reminder.objects.filter(patient=request.user, is_active=True)
    dose_logs = DoseLog.objects.filter(reminder__patient=request.user).order_by('-logged_at')

    context = {
        'patient': patient,
        'prescriptions': prescriptions,
        'reminders': reminders,
        'dose_logs': dose_logs,
    }
    return render(request, 'users/patient_dashboard.html', context)

@login_required
def doctor_adherence(request):
    if request.user.role != 'doctor':
        return redirect('patient_dashboard')

    patients = CustomUser.objects.filter(role='patient')
    adherence_data = []

    for patient in patients:
        logs = DoseLog.objects.filter(
            reminder__patient=patient,
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

    context = {
        'adherence_data': adherence_data,
    }
    return render(request, 'users/doctor_adherence.html', context)


@require_POST
@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')  # or your home page


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
                    subject='Bienvenue sur Medicare',
                    message=(
                        f'Bonjour {user.username},\n\n'
                        'Votre compte patient a été créé avec succès sur la plateforme Medicare.\n'
                        'Vous pouvez maintenant vous connecter, gérer vos traitements et '
                        'trouver des spécialistes adaptés à votre maladie.\n\n'
                        'Ceci est un message automatique, merci de ne pas répondre.'
                    ),
                    from_email=None,            # uses DEFAULT_FROM_EMAIL
                    recipient_list=[user.email],
                    fail_silently=True,         # mets False pour déboguer si besoin
                )
            login(request, user)
            return redirect('dashboard_redirect')  # will send patient to patient_dashboard
    else:
        form = PatientSignUpForm()

    return render(request, 'users/signup.html', {'form': form})