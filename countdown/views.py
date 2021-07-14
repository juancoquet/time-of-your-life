from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import DOBForm, EVENT_DATE_ERROR, EventForm
from .view_helpers import event_is_within_90_yrs_of_dob, get_event_year_of_life, get_event_week_number


def home(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))

    dob_form = DOBForm(request.POST or None)
    if request.method == 'POST':
        if dob_form.is_valid():
            dob = dob_form.cleaned_data['dob']
            return redirect(f'grid/{dob}')
    return render(request, 'home.html', {'dob_form': dob_form})


def grid(request, dob, event_name=None, event_date=None):
    if not DOBForm(data={'dob': dob}).is_valid():
        return redirect('/')

    event_form = EventForm(request.POST or None)
    if request.method == 'POST':
        if event_form.is_valid():
            event_name = event_form.cleaned_data['event_title']
            event_date = event_form.cleaned_data['event_date']
            return redirect(reverse('event', args=[dob, event_name, event_date]))

    dob_form = DOBForm(data={'dob': dob})
    current_year = dob_form.get_current_year_of_life()

    if event_name and event_date:
        event = EventForm(
            data={'event_title': event_name, 'event_date': event_date})
        if not event.is_valid():
            return redirect(reverse('grid', args=[dob]))

        event_date = event.cleaned_data['event_date']
        dob = dob_form.cleaned_data['dob']

        if event_is_within_90_yrs_of_dob(event_date, dob):
            event_year_of_life = get_event_year_of_life(event_date, dob)
            event_week_no = get_event_week_number(event_date, dob)
        else:
            event_form.errors['event_date'] = EVENT_DATE_ERROR
            event_year_of_life = None
            event_week_no = None
    else:
        event_year_of_life = None
        event_week_no = None

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
    user = request.user
    return render(request, 'dashboard.html', {
        'years_passed': user.years_passed,
        'current_year': user.current_year,
        'future_years': user.future_years,
        'full_year_weeks': range(1, 53),
        'weeks_passed_this_yr': user.weeks_passed_this_yr,
        'current_week': user.current_week,
        'weeks_left_this_yr': user.weeks_left_this_yr,
    })
