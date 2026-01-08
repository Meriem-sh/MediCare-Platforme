from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from drugs.models import Disease


class PatientSignUpForm(UserCreationForm):
    phone = forms.CharField(
        max_length=20,
        required=False,
        help_text="Optional. Your phone number."
    )
    disease = forms.ModelChoiceField(
        queryset=Disease.objects.all(),
        required=False,
        help_text="Select your main disease (if known)."
    )
    condition = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Optional. Extra info about your condition."
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone', 'disease', 'condition',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'patient'          # 🔥 force patient role
        user.specialty = None          # patients don’t have a specialty
        # phone, disease, condition are already bound from form
        if commit:
            user.save()
        return user
