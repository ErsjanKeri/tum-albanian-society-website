from django import forms
from .models import ContactUs

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'subject', 'message']
