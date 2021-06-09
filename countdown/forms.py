from django import forms
from datetime import datetime


FUTURE_DOB_ERROR = "Date of birth cannot be in the future"


class DateInput(forms.DateInput):
    input_type = 'date'


class DOBForm(forms.Form):
    dob = forms.DateField(widget=DateInput, label='Date of Birth')

    def clean_dob(self, *args, **kwargs):
        dob_given = self.cleaned_data['dob']
        dob_given = datetime(dob_given.year, dob_given.month, dob_given.day)
        if dob_given >= datetime.today():
            raise forms.ValidationError(FUTURE_DOB_ERROR)
        else:
            return dob_given
