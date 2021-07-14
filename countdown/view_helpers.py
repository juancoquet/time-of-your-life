from datetime import date
from math import ceil


def get_event_year_of_life(event_date, dob):
    try:
        event_date_on_birth_year = date(
            dob.year, event_date.month, event_date.day)
    except ValueError:  # Event day is leap day
        event_date_on_birth_year = date(dob.year, 3, 1)  # Turn into 1st March

    if event_date_on_birth_year < dob:
        event_year_of_life = event_date.year - dob.year
    else:
        event_year_of_life = (event_date.year - dob.year) + 1

    return event_year_of_life


def get_event_week_number(event_date, dob):
    try:
        event_date_on_birth_year = date(
            dob.year, event_date.month, event_date.day)
    except ValueError:  # Event day is leap day
        event_date_on_birth_year = date(dob.year, 3, 1)  # Turn into 1st March
    if event_date_on_birth_year < dob:
        event_date_on_birth_year = date(
            event_date_on_birth_year.year+1,
            event_date_on_birth_year.month,
            event_date_on_birth_year.day
        )

    days_passed = (event_date_on_birth_year - dob).days
    week_no = ceil(days_passed / 7)
    if week_no == 53:
        week_no = 52
    if week_no == 0:
        week_no = 1
    return week_no


def event_is_within_90_yrs_of_dob(event_date, dob):
    try:
        dob_plus_90 = date(dob.year+90, dob.month, dob.day)
    except ValueError:  # dob is leap day
        dob_plus_90 = date(dob.year+90, 3, 1)  # Turn into 1st March
    if event_date > dob_plus_90 or event_date < dob:
        return False
    else:
        return True
