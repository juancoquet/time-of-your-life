import datetime
from django.test import TestCase
from unittest.mock import patch

from countdown import forms
from countdown.forms import DOBForm, FUTURE_DOB_ERROR, is_leap_year


class DOBFormTest(TestCase):

    def test_future_date_is_not_valid(self):
        form = DOBForm(data={'dob': '2999-12-31'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['dob'], [FUTURE_DOB_ERROR])

    def test_past_date_is_valid(self):
        form = DOBForm(data={'dob': '1995-12-01'})
        self.assertTrue(form.is_valid())

    def test_get_current_year_of_life(self):

        class MockToday(datetime.date):
            @classmethod
            def today(cls):
                return cls(2021, 6, 9)

        forms.date = MockToday
        dob = DOBForm(data={'dob': '1995-12-01'})
        self.assertEqual(dob.get_current_year_of_life(), 26)

    def test_get_current_year_of_life_if_today_is_leap_day(self):

        class MockToday(datetime.date):
            @classmethod
            def today(cls):
                return cls(2020, 2, 29)

        forms.date = MockToday

        dob = DOBForm(data={'dob': '2000-02-29'})
        self.assertEqual(dob.get_current_year_of_life(), 21)

    def test_get_current_week_no(self):

        class MockToday(datetime.date):
            @classmethod
            def today(cls):
                return cls(2021, 6, 9)

        forms.date = MockToday

        dob = DOBForm(data={'dob': '1995-12-01'})
        self.assertEqual(dob.get_current_week_no(), 28)
        dob = DOBForm(data={'dob': '2004-02-29'})
        self.assertEqual(dob.get_current_week_no(), 15)
        dob = DOBForm(data={'dob': '2000-6-09'})
        self.assertEqual(dob.get_current_week_no(), 1)
        dob = DOBForm(data={'dob': '2000-6-10'})
        self.assertEqual(dob.get_current_week_no(), 52)

    def test_get_current_week_no_if_today_is_leap_day(self):

        class MockToday(datetime.date):
            @classmethod
            def today(cls):
                return cls(2020, 2, 29)

        forms.date = MockToday

        dob = DOBForm(data={'dob': '1995-12-01'})
        self.assertEqual(dob.get_current_week_no(), 13)
        dob = DOBForm(data={'dob': '1996-12-01'})
        self.assertEqual(dob.get_current_week_no(), 13)
        dob = DOBForm(data={'dob': '2004-02-29'})
        self.assertEqual(dob.get_current_week_no(), 1)
        dob = DOBForm(data={'dob': '2000-03-1'})
        self.assertEqual(dob.get_current_week_no(), 52)


class HelperTest(TestCase):

    def test_is_leap_year(self):
        self.assertTrue(is_leap_year(1916))
        self.assertTrue(is_leap_year(2024))
        self.assertTrue(is_leap_year(2000))
        self.assertTrue(is_leap_year(2400))
        self.assertFalse(is_leap_year(1917))
        self.assertFalse(is_leap_year(2025))
        self.assertFalse(is_leap_year(2100))

