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
            dob = dob_form.cleaned_data['dob']
            return redirect(f'grid/{dob}')
    return render(request, 'home.html', {'dob_form': dob_form})

# TODO: event does not override today week (html change)


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
    event_form = UserEventForm(request.POST or None)
    user = request.user

    if request.method == 'POST':
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.owner = user
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
        event.event_name = form.cleaned_data['event_name']
        event.event_date = form.cleaned_data['event_date']
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
