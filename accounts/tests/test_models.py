import datetime
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

from accounts import models

User = get_user_model()


class CustomUserTest(TestCase):

    ### Helpers ###

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

        models.date = MockToday

    def tearDown(self):
        models.date = datetime.date

    def create_valid_user(self):
        user = User.objects.create(
            username='juan',
            dob='1995-12-01',
            email='test@email.com',
            password='testpass123'
        )
        return user

    ### Tests ###

    def test_new_user_creation(self):
        self.create_valid_user()
        self.assertEqual(len(User.objects.all()), 1)

    def test_usernames_must_be_unique(self):
        self.create_valid_user()
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username='juan',
                dob='1980-12-01',
                email='another@email.com',
                password='testpass123'
            )

    def test_emails_must_be_unique(self):
        self.create_valid_user()
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username='unique',
                dob='1980-12-01',
                email='test@email.com',
                password='testpass123'
            )

    def test_dob_is_required(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username='juan',
                email='test@email.com',
                password='testpass123'
            )

    def test_email_is_required(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username='juan',
                dob='1995-12-01',
                email=None,
                password='testpass123'
            )

    def test_username_is_required(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username=None,
                dob='1995-12-01',
                email='test@email.com',
                password='testpass123'
            )

    def test_current_year_property(self):
        self.patch_datetoday_with_mock()
        self.create_valid_user()
        user = User.objects.first()
        self.assertEqual(user.current_year, 26)

    def test_current_year_property_on_leap_day(self):
        self.patch_datetoday_with_mock(2004, 2, 29)
        self.create_valid_user()
        user = User.objects.first()
        self.assertEqual(user.current_year, 9)

    def test_years_passed_property(self):
        self.patch_datetoday_with_mock()
        self.create_valid_user()
        user = User.objects.first()
        self.assertEqual(len(user.years_passed), 25)

    def test_future_years_property(self):
        self.patch_datetoday_with_mock()
        self.create_valid_user()
        user = User.objects.first()
        self.assertEqual(len(user.future_years), 64)

    def test_current_week_property(self):
        self.patch_datetoday_with_mock()
        self.create_valid_user()
        user = User.objects.first()
        self.assertEqual(user.current_week, 28)

    def test_weeks_passed_this_year(self):
        self.patch_datetoday_with_mock()
        self.create_valid_user()
        user = User.objects.first()
        self.assertEqual(len(user.weeks_passed_this_yr), 27)

    def test_weeks_left_this_year(self):
        self.patch_datetoday_with_mock()
        self.create_valid_user()
        user = User.objects.first()
        self.assertEqual(len(user.weeks_left_this_yr), 24)

    # TODO: Test calendar property
