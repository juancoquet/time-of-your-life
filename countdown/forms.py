from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class DOBForm(forms.Form):
    dob = forms.DateField(widget=DateInput)