
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PrescriptionForm

from .models import Prescription


@login_required
def create_prescription(request):
    if request.user.role != 'doctor':
        return redirect('patient_dashboard')

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = request.user
            prescription.save()
            return redirect('doctor_dashboard')
    else:
        form = PrescriptionForm()

    return render(request, 'prescriptions/create_prescription.html', {'form': form})

@login_required
def edit_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk, doctor=request.user)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')
    else:
        form = PrescriptionForm(instance=prescription)

    return render(request, 'prescriptions/edit_prescription.html', {'form': form, 'prescription': prescription})


@login_required
def delete_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk, doctor=request.user)

    if request.method == 'POST':
        prescription.delete()
        return redirect('doctor_dashboard')

    return render(request, 'prescriptions/confirm_delete_prescription.html', {'prescription': prescription})
