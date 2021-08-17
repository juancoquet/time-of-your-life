import math
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.html import escape
import uuid


class CustomUser(AbstractUser):
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    username = models.CharField(
        primary_key=True,
        max_length=50,
        blank=False,
        null=False,
        unique=True
    )
    day = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(31)
        ]
    )
    month = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12)
        ]
    )
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(2999)
        ]
    )
    dob = models.DateField(blank=False)
    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=False,
        null=False
    )

    REQUIRED_FIELDS = ['dob', 'email']

    ###############
    ### Mehtods ###
    ###############

    def _get_todays_date_on_birth_year(self):
        today = date.today()
        try:
            todays_date_on_birth_year = date(
                self.dob.year, today.month, today.day)
        except ValueError:  # Today is leap day
            todays_date_on_birth_year = date(
                self.dob.year, 3, 1)  # Turn into 1st March
        return todays_date_on_birth_year

    @property
    def current_year(self):
        todays_date_on_birth_year = self._get_todays_date_on_birth_year()

        today = date.today()
        if self.dob > todays_date_on_birth_year:
            current_year = today.year - self.dob.year
        else:
            current_year = (today.year - self.dob.year) + 1

        return current_year

    @property
    def years_passed(self):
        return range(1, self.current_year)

    @property
    def future_years(self):
        return range(self.current_year + 1, 91)

    @property
    def current_week(self):
        todays_date_on_birth_year = self._get_todays_date_on_birth_year()
        if self.dob > todays_date_on_birth_year:
            today = date.today()
            try:
                todays_date_on_birth_year = date(
                    self.dob.year+1, today.month, today.day)
            except ValueError:  # Today is leap day
                todays_date_on_birth_year = date(
                    self.dob.year+1, 3, 1)  # Turn into 1st March

        days_since_bday = (todays_date_on_birth_year - self.dob).days
        week_no = math.ceil(days_since_bday / 7)
        if week_no == 53:
            week_no = 52
        if week_no == 0:
            week_no = 1
        return week_no

    @property
    def weeks_passed_this_yr(self):
        return range(1, self.current_week)

    @property
    def weeks_left_this_yr(self):
        return range(self.current_week + 1, 53)

    @property
    def current_year_and_week(self):
        return (self.current_year, self.current_week)

    @property
    def calendar(self):
        html = '<div class="calendar">'
        events = {}
        for event in self.events.all():
            if not events.get(str(event.index)):
                events[str(event.index)] = [event]
            else:
                events[str(event.index)].append(event)

        for year in range(1, 91):
            html += f'<div class="year-row" id="year-{year}">'
            weeks_in_yr = {}
            for week in range(1, 53):
                if (year, week) < self.current_year_and_week:
                    weeks_in_yr[f'({year}, {week})'] = f'<div class="week past" id="{year}-{week}"><p class="week__number">{week}</p></div>'
                elif (year, week) > self.current_year_and_week:
                    weeks_in_yr[f'({year}, {week})'] = f'<div class="week future" id="{year}-{week}"><p class="week__number">{week}</p></div>'
                else:
                    weeks_in_yr[f'({year}, {week})'] = f'<div class="week present" id="{year}-{week}"><p class="week__number">{week}</p></div>'

            for wk_index, event_iter in events.items():
                if week_element := weeks_in_yr.get(wk_index):
                    up_to_class, classes, id_onwards = week_element.split(
                        '"', 2)
                    classes += " event"
                    with_classes = f'{up_to_class}"{classes}" {id_onwards}'

                    before_event_details = f'<div class="all-tooltips">{with_classes}<div class="tooltip">\
                        <div class="tooltip-content"><div class="arrow"></div><div class="content">'
                    event_details = ''
                    after_event_details = '</div></div></div>'
                    id_ = wk_index.replace(
                        '(', '').replace(')', '').replace(', ', '-')
                    modal = f'<div class="modal-bg" id="modal-bg-{id_}">\
                            <div id="modal-{id_}" class="modal-content">\
                            <div id="close-{id_}" class="close-button">&times</div>'
                    after_modal = '</div></div></div>'

                    for event in event_iter:
                        event_name = escape(event.event_name)
                        event_date = event.event_date.strftime('%b %d, %Y')
                        event_url = event.get_edit_url()
                        event_delete_url = event.get_delete_url()
                        event_yr, event_week = event.index

                        event_details += f'<div class="event_details"><h3>{event_name}</h3><p>{event_date}</p>\
                                <p><a class="tooltip__link" href="{event_url}">Edit</a>\
                                <a class="tooltip__link" href="{event_delete_url}">Delete</a></p></div>'

                        # TODO: multiple modal events
                        modal += f'<h3 class="card__heading">{event_name}</h3><p>{event_date}</p>\
                                <p class="event-metadata">Year {event_yr}, week {event_week}</p>\
                                <p><a class="tooltip__link" href="{event_url}">Edit</a>\
                                <a class="tooltip__link" href="{event_delete_url}">Delete</a></p>'

                    new_element = before_event_details + event_details + \
                        after_event_details + modal + after_modal
                    weeks_in_yr[str(event.index)] = new_element

            for _, value in weeks_in_yr.items():
                html += value
            html += '</div>'
        html += '</div>'
        return html
