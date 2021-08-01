from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ValidationError, DateInput, widgets
from django.utils import timezone
from datetime import date

from countdown.forms import FUTURE_DOB_ERROR, PAST_DOB_ERROR, FUTURE_DOB_ERROR, get_today_minus_90_years


EVENT_OUT_OF_RANGE_ERROR = "Your new date of birth would cause some of your life events" \
    "to be out of range."

VALID_DATE_ERROR = "Please enter a valid date."


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'day', 'month', 'year',)

    # TODO: Handle leaps?
    def clean_year(self, *args, **kwargs):
        day_given = self.cleaned_data['day']
        month_given = self.cleaned_data['month']
        year_given = self.cleaned_data['year']
        try:
            dob_given = date(year_given, month_given, day_given)
        except ValueError:
            raise ValidationError(VALID_DATE_ERROR)
        if dob_given >= timezone.now().date():
            raise ValidationError(FUTURE_DOB_ERROR)
        if dob_given < get_today_minus_90_years().date():
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

    def clean_dob(self, *args, **kwargs):
        dob_given = self.cleaned_data['dob']
        if dob_given >= timezone.now().date():
            raise ValidationError(FUTURE_DOB_ERROR)
        if dob_given < get_today_minus_90_years().date():
            raise ValidationError(PAST_DOB_ERROR)
        else:
            return dob_given

    def show_event_out_of_range_error(self):
        self.errors['dob'] = EVENT_OUT_OF_RANGE_ERROR
