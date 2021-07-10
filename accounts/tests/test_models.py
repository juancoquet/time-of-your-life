from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

User = get_user_model()


class CustomUserTest(TestCase):

    ### Helpers ###

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
                email='test_email.com',
                password='testpass123'
            )
