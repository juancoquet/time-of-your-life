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
            day='01',
            month='12',
            year='1995',
            dob='1995-12-01',
            password='testpass123'
        )
        return User.objects.first()

    ### Tests ###

    def test_valid_event_creation(self):
        user = self.create_user()
        UserEvent.objects.create(
            event_name='test event',
            day='28',
            month='06',
            year='2005',
            event_date='2005-06-28',
            owner=user
        )
        self.assertEqual(len(UserEvent.objects.all()), 1)

    def test_owner_required(self):
        with self.assertRaises(IntegrityError):
            UserEvent.objects.create(
                event_name='test event',
                day='28',
                month='06',
                year='2005',
                event_date='2005-06-28',
                owner=None
            )

    def test_name_required(self):
        with self.assertRaises(IntegrityError):
            UserEvent.objects.create(
                event_name=None,
                day='28',
                month='06',
                year='2005',
                event_date='2005-06-28',
                owner=self.create_user()
            )

    def test_dob_required(self):
        with self.assertRaises(IntegrityError):
            UserEvent.objects.create(
                event_name='test event',
                day='28',
                month='06',
                year='2005',
                event_date=None,
                owner=self.create_user()
            )

    def test_day_required(self):
        with self.assertRaises(IntegrityError):
            UserEvent.objects.create(
                event_name='test event',
                day=None,
                month='06',
                year='2005',
                event_date='2005-06-28',
                owner=self.create_user()
            )

    def test_month_required(self):
        with self.assertRaises(IntegrityError):
            UserEvent.objects.create(
                event_name='test event',
                day='28',
                month=None,
                year='2005',
                event_date='2005-06-28',
                owner=self.create_user()
            )

    def test_year_required(self):
        with self.assertRaises(IntegrityError):
            UserEvent.objects.create(
                event_name='test event',
                day='28',
                month='06',
                year=None,
                event_date='2005-06-28',
                owner=self.create_user()
            )

    def test_FK_relationship(self):
        correct_user = self.create_user()
        User.objects.create(
            username='wronguser',
            email='wrong@user.com',
            day='01',
            month='01',
            year='1980',
            dob='1980-01-01',
            password='testpass123'
        )
        wrong_user = User.objects.get(username='wronguser')
        UserEvent.objects.create(
            event_name='test event',
            day='28',
            month='06',
            year='2005',
            event_date='2005-06-28',
            owner=correct_user
        )
        event = UserEvent.objects.first()
        self.assertEqual(event.owner, correct_user)
        self.assertNotEqual(event.owner, wrong_user)

    def test_event_date_before_user_dob_invalid(self):
        user = self.create_user()
        event = UserEvent(
            event_name='test event',
            day='29',
            month='06',
            year='1940',
            event_date='1940-06-29',
            owner=user
        )
        self.assertFalse(event.is_valid())

    def test_cannot_save_event_before_dob(self):
        user = self.create_user()
        event = UserEvent(
            event_name='test event',
            day='29',
            month='06',
            year='1940',
            event_date='1940-06-29',
            owner=user
        )
        with self.assertRaises(ValidationError):
            event.save_event()

    def test_canot_save_event_more_than_90_years_after_dob(self):
        user = self.create_user()
        event = UserEvent(
            event_name='test event',
            day='29',
            month='06',
            year='2100',
            event_date='2100-06-29',
            owner=user
        )
        with self.assertRaises(ValidationError):
            event.save_event()

    def test_index_returns_correct_yr_wk_tuple(self):
        user = self.create_user()
        event = UserEvent(
            event_name='test event',
            day='29',
            month='01',
            year='2005',
            event_date='2005-01-29',
            owner=user
        )
        self.assertEqual(event.index, (10, 9))
        event = UserEvent(
            event_name='test event',
            day='01',
            month='12',
            year='1995',
            event_date='1995-12-01',
            owner=user
        )
        self.assertEqual(event.index, (1, 1))
        event = UserEvent(
            event_name='test event',
            day='29',
            month='02',
            year='2004',
            event_date='2004-02-29',
            owner=user
        )
        self.assertEqual(event.index, (9, 13))

    def test_get_edit_url(self):
        user = self.create_user()
        event = UserEvent(
            event_name='test event',
            day='29',
            month='01',
            year='2005',
            event_date='2005-01-29',
            owner=user
        )
        event.save_event()
        uuid = event.id
        self.assertEqual(
            event.get_edit_url(),
            f'/grid/edit/{uuid}/'
        )

    def test_get_delete_url(self):
        user = self.create_user()
        event = UserEvent(
            event_name='test event',
            day='29',
            month='01',
            year='2005',
            event_date='2005-01-29',
            owner=user
        )
        event.save_event()
        uuid = event.id
        self.assertEqual(
            event.get_delete_url(),
            f'/grid/delete/{uuid}/'
        )

    def test_cant_create_non_unique_object(self):
        user = self.create_user()
        UserEvent.objects.create(
            event_name='test event',
            day='28',
            month='06',
            year='2005',
            event_date='2005-06-28',
            owner=user
        )
        with self.assertRaises(IntegrityError):
            UserEvent.objects.create(
                event_name='test event',
                day='28',
                month='06',
                year='2005',
                event_date='2005-06-28',
                owner=user
            )
