
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReminderForm, EmailReminderForm
from .models import Reminder
from prescriptions.models import Prescription
from django.utils import timezone
from .models import Reminder, DoseLog

from django.core.mail import send_mail

from django.http import JsonResponse
from datetime import timedelta
from django.db.models import Q


@login_required
def create_reminder(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)

    if request.user.role != 'doctor' or prescription.doctor != request.user:
        return redirect('doctor_dashboard')

    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.prescription = prescription
            reminder.patient = prescription.patient
            reminder.save()
            return redirect('doctor_dashboard')
    else:
        form = ReminderForm()

    return render(request, 'reminders/create_reminder.html', {'form': form, 'prescription': prescription})




@login_required
def mark_dose_taken(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, patient=request.user)

    DoseLog.objects.create(
        reminder=reminder,
        status='taken',
        scheduled_for=timezone.now()
    )

    return redirect('patient_dashboard')


@login_required
def mark_dose_missed(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, patient=request.user)

    DoseLog.objects.create(
        reminder=reminder,
        status='missed',
        scheduled_for=timezone.now()
    )

    return redirect('patient_dashboard')


@login_required
def edit_reminder(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, prescription__doctor=request.user)

    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')
    else:
        form = ReminderForm(instance=reminder)

    return render(request, 'reminders/edit_reminder.html', {'form': form, 'reminder': reminder})


@login_required
def delete_reminder(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, prescription__doctor=request.user)

    if request.method == 'POST':
        reminder.delete()
        return redirect('doctor_dashboard')

    return render(request, 'reminders/confirm_delete_reminder.html', {'reminder': reminder})



@login_required
def email_reminder(request, reminder_id):
    reminder = get_object_or_404(
        Reminder,
        id=reminder_id,
        prescription__doctor=request.user   # only that doctor
    )

    prescription = reminder.prescription
    patient = prescription.patient
    sent = False

    if request.method == "POST":
        form = EmailReminderForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            subject = (
                f"Medication reminder: {prescription.drug.name}"
            )

            message = (
                f"Hello {patient.username},\n\n"
                f"Here is your medication schedule:\n"
                f"- Drug: {prescription.drug.name}\n"
                f"- Dosage: {prescription.dosage}\n"
                f"- Frequency: {prescription.frequency}\n"
                f"- Start: {prescription.start_date}\n"
                f"- End: {prescription.end_date}\n\n"
                f"Doctor's note: {cd.get('comments') or 'No additional comments.'}\n"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=None,           # uses DEFAULT_FROM_EMAIL
                recipient_list=[patient.email],
            )
            sent = True
    else:
        form = EmailReminderForm()

    return render(
        request,
        "reminders/email_reminder.html",
        {
            "form": form,
            "reminder": reminder,
            "patient": patient,
            "sent": sent,
        },
    )

#API for reminders
@login_required
def due_reminders(request):
    """
    JSON API: returns reminders due soon for the logged-in patient.
    Used by JS on the patient dashboard to show pop-up notifications.
    """
    user = request.user

    # Only patients should receive medication reminders
    if getattr(user, "role", None) != "patient":
        return JsonResponse({"reminders": []})

    now = timezone.localtime()
    current_time = now.time()
    window_end_time = (now + timedelta(minutes=10)).time()  # next 10 minutes

    # Because TimeField has no date, we compare only times.
    # Handle the normal case (during the day) and the edge case near midnight.
    if current_time <= window_end_time:
        # e.g. 14:05 -> 14:15
        time_filter = Q(time__gte=current_time, time__lte=window_end_time)
    else:
        # e.g. 23:58 -> 00:08 (wrap around midnight)
        time_filter = Q(time__gte=current_time) | Q(time__lte=window_end_time)

    reminders_qs = Reminder.objects.filter(
        patient=user,
        is_active=True
    ).filter(time_filter).select_related("prescription", "prescription__drug").order_by("time")

    data = []
    for r in reminders_qs:
        prescription = r.prescription
        drug_name = getattr(prescription.drug, "name", "") if prescription and hasattr(prescription, "drug") else ""

        data.append({
            "id": r.id,
            "drug": drug_name,
            "message": f"It is time to take your medication {drug_name}." if drug_name else "It is time to take your medication.",
            "time": r.time.strftime("%H:%M"),
            "dosage": getattr(prescription, "dosage", "") if prescription else "",
            "frequency": getattr(prescription, "frequency", "") if prescription else "",
        })

    return JsonResponse({"reminders": data})
