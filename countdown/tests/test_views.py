from unittest import skip
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http import response
from django.test import TestCase
from django.urls.base import reverse

from countdown.forms import (DOBForm, EventForm, INVALID_DATE_ERROR, UserEventForm,
                             FUTURE_DOB_ERROR, EVENT_DATE_ERROR, DUPLICATE_EVENT_ERROR)
from countdown.models import UserEvent

User = get_user_model()


class HomePageTest(TestCase):

    def test_extends_base_html(self):
        response = self.client.get('/')
        self.assertIn('<title>Time of Your Life</title>',
                      response.content.decode())

    def test_uses_home_page_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_context_includes_dob_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['dob_form'], DOBForm)

    def test_valid_form_POST_redirects_to_grid(self):
        response = self.client.post('/', data={'dob': '1995-12-01'})
        self.assertRedirects(response, '/grid/1995-12-01')

    def test_invalid_form_POST_shows_error(self):
        response = self.client.post('/', data={'dob': '2999-12-31'})
        self.assertContains(response, FUTURE_DOB_ERROR)

    def test_logged_in_user_redirects_to_dashboard(self):
        User.objects.create(
            username='testuser',
            email='test@email.com',
            dob='1995-12-01',
            password='testpass123'
        )
        user = User.objects.first()
        self.client.force_login(user)
        response = self.client.get('/')
        self.assertRedirects(response, reverse('dashboard'))


class GridViewTest(TestCase):

    def test_extends_base_html(self):
        response = self.client.get('/grid/1995-12-01')
        self.assertIn('<title>Time of Your Life</title>',
                      response.content.decode())

    def test_future_dob_url_redirects_home(self):
        response = self.client.get('/grid/2999-12-31')
        self.assertRedirects(response, '/')

    def test_dob_more_than_90_years_ago_redirects_home(self):
        response = self.client.get('/grid/1901-01-01')
        self.assertRedirects(response, '/')

    @patch('countdown.views.DOBForm.get_current_year_of_life')
    def test_context_contains_years_passed_list(self, mock_get_current_year):
        mock_get_current_year.return_value = 26
        response = self.client.get('/grid/1995-12-01')
        self.assertTrue(mock_get_current_year.called)
        self.assertEqual(len(response.context['years_passed']), 25)

    @patch('countdown.views.DOBForm.get_current_year_of_life')
    def test_context_contains_current_year(self, mock_get_current_year):
        mock_get_current_year.return_value = 26
        response = self.client.get('/grid/1995-12-01')
        self.assertTrue(mock_get_current_year.called)
        self.assertEqual(response.context['current_year'], 26)

    @patch('countdown.views.DOBForm.get_current_year_of_life')
    def test_context_contains_future_years_list(self, mock_get_current_year):
        mock_get_current_year.return_value = 26
        response = self.client.get('/grid/1995-12-01')
        self.assertTrue(mock_get_current_year.called)
        self.assertEqual(len(response.context['future_years']), 64)

    @patch('countdown.views.DOBForm.get_current_week_no')
    def test_context_contains_past_weeks_of_this_year_list(self, mock_get_current_week_no):
        mock_get_current_week_no.return_value = 15
        response = self.client.get('/grid/1995-12-01')
        self.assertTrue(mock_get_current_week_no.called)
        self.assertEqual(len(response.context['weeks_passed_this_yr']), 14)

    @patch('countdown.views.DOBForm.get_current_week_no')
    def test_context_contains_future_weeks_of_this_year_list(self, mock_get_current_week_no):
        mock_get_current_week_no.return_value = 15
        response = self.client.get('/grid/1995-12-01')
        self.assertTrue(mock_get_current_week_no.called)
        self.assertEqual(len(response.context['weeks_left_this_yr']), 37)

    def test_grid_contains_90_year_row_divs(self):
        response = self.client.get('/grid/1995-12-01')
        self.assertEqual(
            response.content.decode().count('class="year-row'), 90)

    def test_contains_add_event_section(self):
        response = self.client.get('/grid/1995-12-01')
        self.assertContains(response, 'Add a life event')

    def test_context_contains_event_form(self):
        response = self.client.get('/grid/1995-12-01')
        self.assertIsInstance(response.context['event_form'], EventForm)

    def test_event_date_before_dob_raises(self):
        response = self.client.get('/grid/1995-12-01/test%20event=1995-11-30')
        self.assertContains(response, EVENT_DATE_ERROR)

    def test_event_date_after_90_year_mark_raises(self):
        response = self.client.get('/grid/1995-12-01/test%20event=2085-12-02')
        self.assertContains(response, EVENT_DATE_ERROR)

    def test_event_form_post_uses_grid_template(self):
        response = self.client.post(
            '/grid/1995-12-01',
            data={
                'event_name': 'test event',
                'event_date': '2005-05-31'
            }
        )
        self.assertTemplateUsed(response, 'grid.html')

    def test_context_contains_event_year(self):
        response = self.client.get('/grid/1995-12-01/test%20event=2005-05-31')
        self.assertEqual(response.context['event_year'], 10)

    def test_context_contains_event_week_number(self):
        response = self.client.get('/grid/1999-12-01/test%20event=2005-05-31')
        self.assertEqual(response.context['event_week'], 26)

    def test_context_contains_event_week_number_leap_day_event(self):
        response = self.client.get('/grid/1995-12-01/test%20event=2004-02-29')
        self.assertEqual(response.context['event_week'], 13)

    def test_context_contains_event_week_number_leap_dob(self):
        response = self.client.get('/grid/1996-02-29/test%20event=2005-05-31')
        self.assertEqual(response.context['event_week'], 14)

    def test_faulty_event_date_redirects_to_grid(self):
        response = self.client.get('/grid/1995-12-01/event=not-a-date')
        self.assertRedirects(response, reverse('grid', args=['1995-12-01']))


class DashboardViewTest(TestCase):

    def setUp(self) -> None:
        User.objects.create(
            username='testuser',
            email='test@user.com',
            day='01',
            month='12',
            year='1995',
            dob='1995-12-01',
            password='testpass123'
        )
        self.user = User.objects.first()
        self.client.force_login(self.user)
        self.response = self.client.get('/grid/dashboard/')

    def test_uses_dashboard_template(self):
        self.assertTemplateUsed('dashboard')

    def test_login_required(self):
        self.client.logout()
        response = self.client.get('/grid/dashboard/')
        self.assertRedirects(
            response, '/accounts/login/?account_login=/grid/dashboard/')

    def test_context_contains_current_year(self):
        self.assertIsInstance(self.response.context['current_year'], int)

    def test_context_contains_years_passed_iterable(self):
        self.assertGreater(len(self.response.context['years_passed']), 1)

    def test_context_contains_future_years_iterable(self):
        self.assertGreater(len(self.response.context['future_years']), 1)

    def test_total_years_in_context_equals_90(self):
        years_passed = len(self.response.context['years_passed'])
        future_years = len(self.response.context['future_years'])
        total_years = years_passed + future_years + 1
        self.assertEqual(total_years, 90)

    def test_context_contains_current_week(self):
        self.assertIsInstance(self.response.context['current_week'], int)

    def test_context_contains_weeks_passed_this_yr_iter(self):
        self.assertGreater(
            len(self.response.context['weeks_passed_this_yr']), 1)

    def test_context_contains_weeks_left_this_yr_iter(self):
        self.assertGreater(len(self.response.context['weeks_left_this_yr']), 1)

    def test_context_contains_user_event_form(self):
        self.assertIsInstance(
            self.response.context['user_event_form'],
            UserEventForm
        )

    def test_valid_post_creates_new_event_object(self):
        response = self.client.post('/grid/dashboard/',
                                    data={
                                        'event_name': 'test event',
                                        'day': '29',
                                        'month': '05',
                                        'year': '2004'
                                    }
                                    )
        self.assertEqual(len(UserEvent.objects.all()), 1)

    def test_invalid_post_doesnt_create_new_event_object(self):
        response = self.client.post('/grid/dashboard/',
                                    data={
                                        'event_name': 'test event',
                                        'day': '29',
                                        'month': '05',
                                        'year': '1940'
                                    }
                                    )
        self.assertEqual(len(UserEvent.objects.all()), 0)

    def test_error_shown_on_distant_event_date_post(self):
        response = self.client.post('/grid/dashboard/',
                                    data={
                                        'event_name': 'test event',
                                        'day': '29',
                                        'month': '05',
                                        'year': '2100'
                                    }
                                    )
        self.assertContains(response, EVENT_DATE_ERROR)

    def test_valid_post_creates_event_for_correct_owner(self):
        User.objects.create(
            username='wronguser',
            day='01',
            month='12',
            year='1995',
            dob='1995-12-01',
            password='testpass123',
            email='wronguser@email.com'
        )
        correct_user = User.objects.get(username='testuser')
        wrong_user = User.objects.get(username='wronguser')
        response = self.client.post('/grid/dashboard/',
                                    data={
                                        'event_name': 'test event',
                                        'day': '29',
                                        'month': '05',
                                        'year': '2005'
                                    }
                                    )
        event = UserEvent.objects.first()
        self.assertEqual(event.owner, correct_user)
        self.assertNotEqual(event.owner, wrong_user)

    def test_invalid_day_raises_error(self):
        response = self.client.post('/grid/dashboard/',
                                    data={
                                        'event_name': 'test event',
                                        'day': '29999',
                                        'month': '05',
                                        'year': '2005'
                                    }
                                    )
        self.assertContains(response, INVALID_DATE_ERROR)

    def test_invalid_month_raises_error(self):
        response = self.client.post('/grid/dashboard/',
                                    data={
                                        'event_name': 'test event',
                                        'day': '29',
                                        'month': '05999',
                                        'year': '2005'
                                    }
                                    )
        self.assertContains(response, INVALID_DATE_ERROR)

    def test_invalid_year_raises_error(self):
        response = self.client.post('/grid/dashboard/',
                                    data={
                                        'event_name': 'test event',
                                        'day': '29',
                                        'month': '05',
                                        'year': '399999'
                                    }
                                    )
        self.assertContains(response, INVALID_DATE_ERROR)


class EventUpdateViewTest(TestCase):

    def setUp(self):
        User.objects.create(
            username='testuser',
            dob='1995-12-01',
            password='testpass123',
            email='test@user.com'
        )
        self.user = User.objects.first()
        UserEvent.objects.create(
            event_name='test event',
            event_date='2005-05-29',
            owner=self.user
        )
        self.event = UserEvent.objects.first()
        self.client.force_login(self.user)

    def test_change_event_name(self):
        self.client.post(
            self.event.get_edit_url(),
            data={
                'event_name': 'changed event',
                'event_date': '2009-05-29'
            }
        )
        self.event = UserEvent.objects.first()
        self.assertEqual(self.event.event_name, 'changed event')
        self.assertEqual(self.event.event_date.year, 2009)

    def test_edit_doesnt_create_new_event(self):
        self.assertEqual(len(UserEvent.objects.all()), 1)
        self.client.post(
            self.event.get_edit_url(),
            data={
                'event_name': 'changed event',
                'event_date': '2009-05-29'
            }
        )
        self.assertEqual(len(UserEvent.objects.all()), 1)

    def test_invalid_date_shows_error(self):
        response = self.client.post(
            self.event.get_edit_url(),
            data={
                'event_name': 'changed event',
                'event_date': '2109-05-29'
            }
        )
        self.assertContains(response, EVENT_DATE_ERROR)

    def test_non_date_shows_error(self):
        response = self.client.post(
            self.event.get_edit_url(),
            data={
                'event_name': 'changed event',
                'event_date': 'abcdefg'
            }
        )
        self.assertContains(response, 'Enter a valid date')

    def test_only_event_owner_can_edit(self):
        wrong_user = User.objects.create(
            username='wronguser',
            email='wrong@user.com',
            dob='2000-01-01',
            password='testpass123'
        )
        self.client.force_login(wrong_user)
        response = self.client.get(self.event.get_edit_url())
        self.assertEqual(response.status_code, 403)

    def test_valid_post_redirects(self):
        response = self.client.post(
            self.event.get_edit_url(),
            data={
                'event_name': 'changed event',
                'event_date': '2009-05-29'
            }
        )
        self.assertEqual(response.status_code, 302)


class EventDeleteViewTest(TestCase):

    def setUp(self):
        User.objects.create(
            username='testuser',
            dob='1995-12-01',
            password='testpass123',
            email='test@user.com'
        )
        self.user = User.objects.first()
        UserEvent.objects.create(
            event_name='test event',
            event_date='2005-05-29',
            owner=self.user
        )
        self.event = UserEvent.objects.first()
        self.client.force_login(self.user)

    def test_only_event_owner_can_delete(self):
        User.objects.create(
            username='wronguser',
            dob='2001-01-19',
            password='testpass123',
            email='wrong@user.com'
        )
        wrong_user = User.objects.get(username='wronguser')
        self.client.force_login(wrong_user)
        response = self.client.get(self.event.get_delete_url())
        self.assertEqual(response.status_code, 403)

    def test_page_uses_correct_event(self):
        UserEvent.objects.create(
            event_name='wrong event',
            event_date='1999-05-29',
            owner=self.user
        )
        wrong_event = UserEvent.objects.all()[1]
        response = self.client.get(self.event.get_delete_url())
        self.assertEqual(response.context['event'], self.event)
        self.assertNotEqual(response.context['event'], wrong_event)

    def test_post_deletes_event(self):
        self.client.post(self.event.get_delete_url())
        self.assertEqual(len(UserEvent.objects.all()), 0)

    def test_post_deletes_correct_event(self):
        UserEvent.objects.create(
            event_name='delete event',
            event_date='1999-05-29',
            owner=self.user
        )
        self.assertEqual(len(UserEvent.objects.all()), 2)
        delete_event = UserEvent.objects.all()[1]

        self.client.post(delete_event.get_delete_url())
        self.assertEqual(len(UserEvent.objects.all()), 1)

        remaining_event = UserEvent.objects.first()
        self.assertEqual(remaining_event, self.event)
        self.assertNotEqual(remaining_event, delete_event)
