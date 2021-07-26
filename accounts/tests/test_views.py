from countdown.models import UserEvent
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from unittest.case import skip

from accounts.forms import CustomUserChangeForm, FUTURE_DOB_ERROR, PAST_DOB_ERROR, EVENT_OUT_OF_RANGE_ERROR

User = get_user_model()


class SignupViewTest(TestCase):

    def test_signup_page_uses_signup_template(self):
        response = self.client.get('/accounts/signup/')
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_form_fields_are_present(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(
            response.content.decode().count('class="form_field"'),
            6)

    def test_username_required(self):
        response = self.client.post('/accounts/signup/',
                                    data={
                                        'email': 'test@email.com',
                                        'name': 'juan',
                                        'dob': '1995-12-01',
                                        'password1': 'testpass123',
                                        'password2': 'testpass123'
                                    }
                                    )
        self.assertContains(response, 'This field is required')

    def test_email_required(self):
        response = self.client.post('/accounts/signup/',
                                    data={
                                        'username': 'juan',
                                        'name': 'juan',
                                        'dob': '1995-12-01',
                                        'password1': 'testpass123',
                                        'password2': 'testpass123'
                                    }
                                    )
        self.assertContains(response, 'This field is required')

    def test_dob_required(self):
        response = self.client.post('/accounts/signup/',
                                    data={
                                        'username': 'juan',
                                        'email': 'test@email.com',
                                        'name': 'juan',
                                        'password1': 'testpass123',
                                        'password2': 'testpass123'
                                    }
                                    )
        self.assertContains(response, 'This field is required')

    def test_future_dob_shows_error(self):
        response = self.client.post('/accounts/signup/',
                                    data={
                                        'username': 'juan',
                                        'email': 'test@email.com',
                                        'name': 'juan',
                                        'dob': '2999-12-01',
                                        'password1': 'testpass123',
                                        'password2': 'testpass123'
                                    }
                                    )
        self.assertContains(response, FUTURE_DOB_ERROR)

    def test_dob_more_than_90_year_ago_shows_error(self):
        response = self.client.post('/accounts/signup/',
                                    data={
                                        'username': 'juan',
                                        'email': 'test@email.com',
                                        'name': 'juan',
                                        'dob': '1901-12-01',
                                        'password1': 'testpass123',
                                        'password2': 'testpass123'
                                    }
                                    )
        self.assertContains(response, PAST_DOB_ERROR)

    def test_duplicate_username_shows_error(self):
        User.objects.create(
            username='juan',
            dob='1995-12-01',
            email='test@email.com',
            password='testpass123'
        )
        response = self.client.post('/accounts/signup/',
                                    data={
                                        'username': 'juan',
                                        'email': 'other@email.com',
                                        'name': 'juan',
                                        'dob': '1995-12-01',
                                        'password1': 'testpass123',
                                        'password2': 'testpass123'
                                    }
                                    )
        self.assertContains(response, 'User with this Username already exists')

    def test_duplicate_email_shows_error(self):
        User.objects.create(
            username='juan',
            dob='1995-12-01',
            email='test@email.com',
            password='testpass123'
        )
        response = self.client.post('/accounts/signup/',
                                    data={
                                        'username': 'juanc',
                                        'email': 'test@email.com',
                                        'name': 'juan',
                                        'dob': '1995-12-01',
                                        'password1': 'testpass123',
                                        'password2': 'testpass123'
                                    }
                                    )
        self.assertContains(response, 'User with this Email already exists')

    def test_valid_post_creates_user(self):
        self.assertEqual(User.objects.all().count(), 0)
        self.client.post('/accounts/signup/',
                         data={
                             'username': 'juan',
                             'email': 'test@email.com',
                             'name': 'juan',
                             'dob': '1995-12-01',
                             'password1': 'testpass123',
                             'password2': 'testpass123'
                         }
                         )
        self.assertEqual(User.objects.all().count(), 1)


class ProfileViewTest(TestCase):

    def setUp(self):
        User.objects.create(
            username='testuser',
            dob='1995-12-01',
            email='test@user.com',
            password='testpass123'
        )
        self.user = User.objects.first()
        self.client.force_login(self.user)
        self.response = self.client.get(
            reverse('profile', kwargs={'pk': self.user.username}))

    def test_contains_user_change_form(self):
        self.assertIsInstance(
            self.response.context['form'], CustomUserChangeForm)

    def test_only_correct_user_can_access_profile(self):
        User.objects.create(
            username='wronguser',
            dob='2000-05-29',
            email='wrong@user.com',
            password='testpass123'
        )
        wrong_user = User.objects.get(username='wronguser')
        response = self.client.get(
            reverse('profile', kwargs={'pk': wrong_user.username})
        )
        self.assertEqual(response.status_code, 403)

    def test_contains_password_change_link(self):
        self.assertIn(
            reverse('account_change_password'),
            self.response.content.decode()
        )

    def test_dob_change_cant_leave_event_out_of_range(self):
        UserEvent.objects.create(
            event_name='test event',
            event_date='2005-04-29',
            owner=self.user
        )
        response = self.client.post(
            reverse('profile', kwargs={'pk': self.user.username}),
            data={
                'email': 'test@user.com',
                'dob': '2006-12-01',
                'name': 'test'
            }
        )
        self.assertIn(EVENT_OUT_OF_RANGE_ERROR, response.content.decode())
