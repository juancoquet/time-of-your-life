from django.core.exceptions import ValidationError
from countdown.forms import UserEventForm
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from unittest import skip

from countdown.models import UserEvent

User = get_user_model()


class UserEventModelTest(TestCase):

    ### Helpers ###

    def create_user(self):
        User.objects.create(
            username='testuser',
            email='test@user.com',
            dob='1995-12-01',
            password='testpass123'
        )
        return User.objects.first()

    ### Tests ###

    def test_valid_event_creation(self):
        user = self.create_user()
        UserEvent.objects.create(
            event_name='test event',
            event_date='2005-06-28',
            owner=user
        )
        self.assertEqual(len(UserEvent.objects.all()), 1)

    def test_owner_required(self):
        with self.assertRaises(IntegrityError):
            UserEvent.objects.create(
                event_name='test event',
                event_date='2005-06-28',
                owner=None
            )

    def test_name_required(self):
        with self.assertRaises(IntegrityError):
            UserEvent.objects.create(
                event_name=None,
                event_date='2005-06-28',
                owner=self.create_user()
            )

    def test_date_required(self):
        with self.assertRaises(IntegrityError):
            UserEvent.objects.create(
                event_name='test event',
                event_date=None,
                owner=self.create_user()
            )

    def test_FK_relationship(self):
        correct_user = self.create_user()
        User.objects.create(
            username='wronguser',
            email='wrong@user.com',
            dob='1980-01-01',
            password='testpass123'
        )
        wrong_user = User.objects.get(username='wronguser')
        UserEvent.objects.create(
            event_name='test event',
            event_date='2005-06-29',
            owner=correct_user
        )
        event = UserEvent.objects.first()
        self.assertEqual(event.owner, correct_user)
        self.assertNotEqual(event.owner, wrong_user)

    def test_event_date_before_user_dob_invalid2(self):
        user = self.create_user()
        event = UserEvent(
            event_name='test event',
            event_date='1940-06-29',
            owner=user
        )
        self.assertFalse(event.is_valid())

    def test_cannot_save_event_before_dob(self):
        user = self.create_user()
        event = UserEvent(
            event_name='test event',
            event_date='1940-06-29',
            owner=user
        )
        with self.assertRaises(ValidationError):
            event.save_event()

    def test_canot_save_event_more_than_90_years_after_dob(self):
        user = self.create_user()
        event = UserEvent(
            event_name='test event',
            event_date='2100-06-29',
            owner=user
        )
        with self.assertRaises(ValidationError):
            event.save_event()

    def test_index_returns_correct_yr_wk_tuple(self):
        user = self.create_user()
        event = UserEvent(
            event_name='test event',
            event_date='2005-01-29',
            owner=user
        )
        self.assertEqual(event.index, (10, 9))
        event = UserEvent(
            event_name='test event',
            event_date='1995-12-01',
            owner=user
        )
        self.assertEqual(event.index, (1, 1))
        event = UserEvent(
            event_name='test event',
            event_date='2004-02-29',
            owner=user
        )
        self.assertEqual(event.index, (9, 13))
