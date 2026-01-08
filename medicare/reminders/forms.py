from django import forms
from .models import Reminder

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['time', 'is_active']


class EmailReminderForm(forms.Form):
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

