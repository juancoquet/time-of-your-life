from django.test import TestCase
from unittest.mock import patch
from unittest import skip

from countdown.forms import DOBForm, FUTURE_DOB_ERROR


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
