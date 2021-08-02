from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm, FUTURE_DOB_ERROR, PAST_DOB_ERROR, VALID_DATE_ERROR

User = get_user_model()


class CreationFormTest(TestCase):

    def test_valid_user_form(self):
        form = CustomUserCreationForm(
            data={
                'username': 'juan',
                'email': 'test@email.com',
                'password1': 'testpass123',
                'password2': 'testpass123',
                'day': '01',
                'month': '12',
                'year': '1995'
            }
        )
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_cannot_have_future_dob(self):
        form = CustomUserCreationForm(
            data={
                'username': 'juan',
                'email': 'test@email.com',
                'password1': 'testpass123',
                'password2': 'testpass23',
                'day': '01',
                'month': '12',
                'year': '2100'
            }
        )
        form.full_clean()
        self.assertEqual(form.errors['year'], [FUTURE_DOB_ERROR])

    def test_dob_more_than_90_years_ago_is_not_valid(self):
        form = CustomUserCreationForm(
            data={
                'username': 'juan',
                'email': 'test@email.com',
                'password1': 'testpass123',
                'password2': 'testpass23',
                'day': '01',
                'month': '12',
                'year': '1905'
            }
        )
        form.full_clean()
        self.assertEqual(form.errors['year'], [PAST_DOB_ERROR])

    def test_successful_form_creates_new_user(self):
        form = CustomUserCreationForm(
            data={
                'username': 'juan',
                'email': 'test@email.com',
                'password1': 'testpass123',
                'password2': 'testpass123',
                'day': '01',
                'month': '12',
                'year': '1995'
            }
        )
        form.save()
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(User.objects.first().dob, date(1995, 12, 1))

    def test_invalid_date(self):
        form = CustomUserCreationForm(
            data={
                'username': 'juan',
                'email': 'test@email.com',
                'password1': 'testpass123',
                'password2': 'testpass123',
                'day': '29',
                'month': '02',
                'year': '1995'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['year'], [VALID_DATE_ERROR])

    def test_leap_day_allowed(self):
        form = CustomUserCreationForm(
            data={
                'username': 'juan',
                'email': 'test@email.com',
                'password1': 'testpass123',
                'password2': 'testpass123',
                'day': '29',
                'month': '02',
                'year': '2004'
            }
        )
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(User.objects.first().dob, date(2004, 2, 29))


class UserChangeFormTest(TestCase):

    def test_valid_change_form(self):
        form = CustomUserChangeForm(
            data={
                'email': 'new@email.com',
                'first_name': 'test',
                'day': '07',
                'month': '01',
                'year': '2007'
            }
        )
        self.assertTrue(form.is_valid())
