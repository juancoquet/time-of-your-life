from accounts.forms import EVENT_OUT_OF_RANGE_ERROR
from datetime import date
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import DeleteView, UpdateView

from countdown.models import UserEvent
from .forms import DOBForm, EVENT_DATE_ERROR, EventForm, UserEventForm
from .view_helpers import event_is_within_90_yrs_of_dob, get_event_year_of_life, get_event_week_number


def home(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))

    dob_form = DOBForm(request.POST or None)
    if request.method == 'POST':
        if dob_form.is_valid():
            day = dob_form.cleaned_data['day']
            month = dob_form.cleaned_data['month']
            year = dob_form.cleaned_data['year']
            dob = date(year, month, day)
            return redirect(f'grid/{dob}')
    return render(request, 'home.html', {'dob_form': dob_form})


def grid(request, dob, event_name=None, day=None, month=None, year=None):
    dob_year, dob_month, dob_day = dob.split('-')
    dob_form = DOBForm(
        data={
            'day': dob_day,
            'month': dob_month,
            'year': dob_year
        }
    )
    if not dob_form.is_valid():
        return redirect('/')

    event_form = EventForm(request.POST or None)
    if request.method == 'POST':
        if event_form.is_valid():
            event_name = event_form.cleaned_data['event_title']
            day = event_form.cleaned_data['day']
            month = event_form.cleaned_data['month']
            year = event_form.cleaned_data['year']
            return redirect(reverse('event', args=[dob, event_name, day, month, year]))

    current_year = dob_form.get_current_year_of_life()

    if event_name and day and month and year:
        event_form = EventForm(
            data={
                'event_title': event_name,
                'day': day,
                'month': month,
                'year': year
            }
        )
        if not event_form.is_valid():
            return redirect(reverse('grid', args=[dob]))

        event_date = date(year, month, day)
        dob_day, dob_month, dob_year = dob_form.cleaned_data.values()
        dob = date(dob_year, dob_month, dob_day)

        if event_is_within_90_yrs_of_dob(event_date, dob):
            event_year_of_life = get_event_year_of_life(event_date, dob)
            event_week_no = get_event_week_number(event_date, dob)
        else:
            event_form.errors['year'] = EVENT_DATE_ERROR
            event_year_of_life = None
            event_week_no = None
    else:
        event_year_of_life = None
        event_week_no = None
        event_date = None

    return render(request, 'grid.html', {
        'years_passed': range(1, current_year),
        'current_year': current_year,
        'future_years': range(current_year + 1, 91),
        'full_year_weeks': range(1, 53),
        'weeks_passed_this_yr': range(1, dob_form.get_current_week_no()),
        'current_week': dob_form.get_current_week_no(),
        'weeks_left_this_yr': range(dob_form.get_current_week_no() + 1, 53),
        'event_form': event_form,
        'date_of_birth': dob,
        'event_year': event_year_of_life,
        'event_week': event_week_no,
        'event_name': event_name,
        'event_date': event_date,
    })


@login_required(redirect_field_name='account_login')
def dashboard(request):
    event_form = UserEventForm(request.POST or None)
    user = request.user

    if request.method == 'POST':
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.owner = user
            day_given = event_form.cleaned_data['day']
            month_given = event_form.cleaned_data['month']
            year_given = event_form.cleaned_data['year']
            event.event_date = date(year_given, month_given, day_given)
            try:
                event.save_event()
            except ValidationError:
                event_form.show_event_date_error()
            except IntegrityError:
                event_form.show_unique_restraint_error()

    return render(request, 'dashboard.html', {
        'years_passed': user.years_passed,
        'current_year': user.current_year,
        'future_years': user.future_years,
        'full_year_weeks': range(1, 53),
        'weeks_passed_this_yr': user.weeks_passed_this_yr,
        'current_week': user.current_week,
        'weeks_left_this_yr': user.weeks_left_this_yr,
        'user_event_form': event_form,
        'calendar': user.calendar
    })


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = UserEvent
    form_class = UserEventForm
    login_url = 'account_login'
    template_name = 'edit_event.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != self.request.user:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        event = self.get_object()
        if not form.is_valid():
            return self.form_invalid(form)
        event = form.save(commit=False)
        if event.is_valid():
            event.save_event()
            return redirect('/')
        else:
            form.show_event_date_error()
            return self.form_invalid(form)


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = UserEvent
    success_url = '/'
    template_name = 'delete_event.html'
    context_object_name = 'event'
    login_url = 'account_login'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != self.request.user:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)
