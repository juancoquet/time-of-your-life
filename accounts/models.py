import math
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=50, blank=False, null=False, unique=True)
    dob = models.DateField(blank=False)
    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=False,
        null=False
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['dob', 'username']

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

    # TODO: Create calendar @property to generate weeks iter

    @property
    def calendar(self):
        html = '<table>'
        for year in range(1, 91):
            html += f'<tr class="year" id="year-{year}">'
            weeks = {}
            for week in range(1, 53):
                if (year, week) < self.current_year_and_week:
                    weeks[f'({year}, {week})'] = f'<td class="week past" id="({year},{week})">{week}</td>'
                elif (year, week) > self.current_year_and_week:
                    weeks[f'({year}, {week})'] = f'<td class="week future" id="({year},{week})">{week}</td>'
                else:
                    weeks[f'({year}, {week})'] = f'<td class="week present" id="({year},{week})">{week}</td>'
            for event in self.events.all():
                event_date = event.event_date.strftime('%b %w, %Y')
                if week_element := weeks.get(str(event.index)):
                    up_to_class, classes, id_onwards = week_element.split(
                        '"', 2)
                    classes += " event"
                    with_classes = f'{up_to_class}"{classes}" {id_onwards}'
                    wihtout_closing_tag, closing_tag = with_classes.split('</')
                    new_element = f'{wihtout_closing_tag}<div class="all-tooltips"><div class="tooltip">\
                        <div class="tooltip-content"><div class="arrow"></div><div class="content">\
                        <h3>{event.event_name}</h3><p>{event_date}</p><p class="edit">Edit</p>\
                        </div></div></div></div>'
                    weeks[str(event.index)] = new_element
            for _, value in weeks.items():
                html += value
            html += '</tr>'
        html += '</table>'
        return html
