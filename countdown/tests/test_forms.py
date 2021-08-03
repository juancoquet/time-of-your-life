import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from unittest.mock import patch

from countdown import forms
from countdown.forms import (DOBForm, EVENT_DATE_ERROR, EventForm, INVALID_DATE_ERROR, UserEventForm,
                             FUTURE_DOB_ERROR, PAST_DOB_ERROR, is_leap_year)
from countdown.models import UserEvent

User = get_user_model()


class DOBFormTest(TestCase):

    @staticmethod
    def patch_datetoday_with_mock(year=2021, month=6, day=9):
        """
        For testing: makes date.today() return a date object on 2021-06-09 (y-m-d) by default, or provide custom values.
        Couldn't use @patch decorator as the .today attribute can't be overwritten.

        :return: datetime.date object on the given date when forms.date.today() is called.
        """

        class MockToday(datetime.date):
            @classmethod
            def today(cls):
                return cls(year, month, day)

        forms.date = MockToday

    def tearDown(self):
        forms.date = datetime.date

    def test_future_date_is_not_valid(self):
        form = DOBForm(data={'dob': '2999-12-31'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['dob'], [FUTURE_DOB_ERROR])

    def test_dob_more_than_90_years_ago_is_not_valid(self):
        form = DOBForm(data={'dob': '1901-01-01'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['dob'], [PAST_DOB_ERROR])

    def test_past_date_is_valid(self):
        form = DOBForm(data={'dob': '1995-12-01'})
        self.assertTrue(form.is_valid())

    def test_get_current_year_of_life(self):
        self.patch_datetoday_with_mock()

        dob = DOBForm(data={'dob': '1995-12-01'})
        self.assertEqual(dob.get_current_year_of_life(), 26)

    def test_get_current_year_of_life_if_today_is_leap_day(self):
        self.patch_datetoday_with_mock(2020, 2, 29)

        dob = DOBForm(data={'dob': '2000-02-29'})
        self.assertEqual(dob.get_current_year_of_life(), 21)

    def test_get_current_week_no(self):
        self.patch_datetoday_with_mock()

        dob = DOBForm(data={'dob': '1995-12-01'})
        self.assertEqual(dob.get_current_week_no(), 28)
        dob = DOBForm(data={'dob': '2004-02-29'})
        self.assertEqual(dob.get_current_week_no(), 15)
        dob = DOBForm(data={'dob': '2000-6-09'})
        self.assertEqual(dob.get_current_week_no(), 1)
        dob = DOBForm(data={'dob': '2000-6-10'})
        self.assertEqual(dob.get_current_week_no(), 52)

    def test_get_current_week_no_if_today_is_leap_day(self):
        self.patch_datetoday_with_mock(2020, 2, 29)

        dob = DOBForm(data={'dob': '1995-12-01'})
        self.assertEqual(dob.get_current_week_no(), 13)
        dob = DOBForm(data={'dob': '1996-12-01'})
        self.assertEqual(dob.get_current_week_no(), 13)
        dob = DOBForm(data={'dob': '2004-02-29'})
        self.assertEqual(dob.get_current_week_no(), 1)
        dob = DOBForm(data={'dob': '2000-03-1'})
        self.assertEqual(dob.get_current_week_no(), 52)

    def test_yields_weeks_passed_iter(self):
        dob = DOBForm(data={'dob': '1995-12-01'})
        self.patch_datetoday_with_mock()
        self.assertEqual(len(dob.weeks_passed), (25*52) + 27)


class EventFormTest(TestCase):

    def test_valid_past_date(self):
        form = EventForm(
            data={
                'event_title': 'test event',
                'day': '31',
                'month': '05',
                'year': '2005'
            }
        )
        self.assertTrue(form.is_valid())

    def test_valid_future_date(self):
        form = EventForm(
            data={
                'event_title': 'test event',
                'day': '31',
                'month': '05',
                'year': '2065'
            }
        )
        self.assertTrue(form.is_valid())

    def test_day_out_of_range(self):
        form = EventForm(
            data={
                'event_title': 'test event',
                'day': '32',
                'month': '05',
                'year': '2005'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['year'], INVALID_DATE_ERROR)
        form = EventForm(
            data={
                'event_title': 'test event',
                'day': '-1',
                'month': '05',
                'year': '2005'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['year'], INVALID_DATE_ERROR)

    def test_month_out_of_range(self):
        form = EventForm(
            data={
                'event_title': 'test event',
                'day': '19',
                'month': '13',
                'year': '2005'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['year'], INVALID_DATE_ERROR)
        form = EventForm(
            data={
                'event_title': 'test event',
                'day': '19',
                'month': '-1',
                'year': '2005'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['year'], INVALID_DATE_ERROR)

    def test_past_date_greater_than_90_years_ago_not_valid(self):
        form = EventForm(
            data={
                'event_title': 'test event',
                'day': '31',
                'month': '05',
                'year': '1901'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['year'], EVENT_DATE_ERROR)


class HelperTest(TestCase):

    def test_is_leap_year(self):
        self.assertTrue(is_leap_year(1916))
        self.assertTrue(is_leap_year(2024))
        self.assertTrue(is_leap_year(2000))
        self.assertTrue(is_leap_year(2400))
        self.assertFalse(is_leap_year(1917))
        self.assertFalse(is_leap_year(2025))
        self.assertFalse(is_leap_year(2100))


class UserEventFormTest(TestCase):

    def test_valid_form(self):
        form = UserEventForm(
            data={
                'event_name': 'test event',
                'day': '28',
                'month': '05',
                'year': '2001'
            }
        )
        self.assertTrue(form.is_valid())

    def test_save_creates_object_with_day_month_year(self):
        form = UserEventForm(
            data={
                'event_name': 'test event',
                'day': '28',
                'month': '05',
                'year': '2001'
            }
        )
        event = form.save(commit=False)
        self.assertEqual(event.day, 28)
        self.assertEqual(event.month, 5)
        self.assertEqual(event.year, 2001)

    def test_invalid_day(self):
        form = UserEventForm(
            data={
                'event_name': 'test event',
                'day': '28999',
                'month': '05',
                'year': '2001'
            }
        )
        self.assertFalse(form.is_valid())

    def test_invalid_month(self):
        form = UserEventForm(
            data={
                'event_name': 'test event',
                'day': '28',
                'month': '05999',
                'year': '2001'
            }
        )
        self.assertFalse(form.is_valid())

    def test_invalid_year(self):
        form = UserEventForm(
            data={
                'event_name': 'test event',
                'day': '28',
                'month': '05',
                'year': '212341'
            }
        )
        self.assertFalse(form.is_valid())
