from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ValidationError, DateInput, widgets
from django.utils import timezone
from datetime import date

from countdown.forms import FUTURE_DOB_ERROR, PAST_DOB_ERROR, FUTURE_DOB_ERROR, get_today_minus_90_years


EVENT_OUT_OF_RANGE_ERROR = "Your new date of birth would cause some of your life events" \
    " to be out of range."

VALID_DATE_ERROR = "Please enter a valid date."


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'day', 'month', 'year')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Username*'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input',
                'placeholder': 'Email*'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Name'
            }),
            'day': forms.NumberInput(attrs={
                'class': 'input input--int',
                'placeholder': 'DD*',
            }),
            'month': forms.NumberInput(attrs={
                'class': 'input input--int',
                'placeholder': 'MM*',
            }),
            'year': forms.NumberInput(attrs={
                'class': 'input input--int',
                'placeholder': 'YYYY*',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'input', 'placeholder': 'Password*'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'input', 'placeholder': 'Confirm password*'})

    def clean_year(self, *args, **kwargs):
        try:
            day_given = self.cleaned_data['day']
            month_given = self.cleaned_data['month']
            year_given = self.cleaned_data['year']
        except KeyError:
            raise ValidationError(VALID_DATE_ERROR)
        try:
            dob_given = date(year_given, month_given, day_given)
        except ValueError:
            raise ValidationError(VALID_DATE_ERROR)
        if dob_given >= timezone.now().date():
            raise ValidationError(FUTURE_DOB_ERROR)
        if dob_given < get_today_minus_90_years():
            raise ValidationError(PAST_DOB_ERROR)
        else:
            return year_given

    def save(self, commit=True):
        user = super().save(commit=False)
        day_given = self.cleaned_data['day']
        month_given = self.cleaned_data['month']
        year_given = self.cleaned_data['year']
        user.dob = date(year_given, month_given, day_given)
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'day', 'month', 'year',)
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'input',
                'placeholder': 'Email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Name'
            }),
            'day': forms.NumberInput(attrs={
                'class': 'input input--int',
                'placeholder': 'DD',
            }),
            'month': forms.NumberInput(attrs={
                'class': 'input input--int',
                'placeholder': 'MM',
            }),
            'year': forms.NumberInput(attrs={
                'class': 'input input--int',
                'placeholder': 'YYYY',
            }),
        }

    def clean_year(self, *args, **kwargs):
        try:
            day_given = self.cleaned_data['day']
            month_given = self.cleaned_data['month']
            year_given = self.cleaned_data['year']
        except KeyError:
            raise ValidationError(VALID_DATE_ERROR)
        try:
            dob_given = date(year_given, month_given, day_given)
        except ValueError:
            raise ValidationError(VALID_DATE_ERROR)
        if dob_given >= timezone.now().date():
            raise ValidationError(FUTURE_DOB_ERROR)
        if dob_given < get_today_minus_90_years():
            raise ValidationError(PAST_DOB_ERROR)
        else:
            return year_given

    def save(self, commit=True):
        user = super().save(commit=False)
        day_given = self.cleaned_data['day']
        month_given = self.cleaned_data['month']
        year_given = self.cleaned_data['year']
        user.dob = date(year_given, month_given, day_given)
        if commit:
            user.save()
        return user

    def show_event_out_of_range_error(self):
        self.errors['year'] = EVENT_OUT_OF_RANGE_ERROR
