from django import forms
from django.utils import timezone

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
        }

    def clean_start_date(self):
        start = self.cleaned_data["start_date"]
        if start < timezone.localdate():
            raise forms.ValidationError("Start date cannot be in the past.")
        return start