from django.test import TestCase

from countdown.forms import DOBForm, FUTURE_DOB_ERROR


class HomePageTest(TestCase):

    def test_extends_base_html(self):
        response = self.client.get('/')
        self.assertIn('<title>Time of Your Life</title>', response.content.decode())

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
        self.assertIn('<title>Time of Your Life</title>', response.content.decode())