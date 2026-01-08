from django import forms
from .models import Prescription
from users.models import CustomUser

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'drug', 'dosage', 'frequency', 'start_date', 'end_date', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # only show patients, not doctors
        self.fields['patient'].queryset = CustomUser.objects.filter(role='patient')
