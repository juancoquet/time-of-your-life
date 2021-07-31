from django import forms

from .models import Feedback, Contact


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ('subject', 'message', 'email')


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('subject', 'message', 'email')
