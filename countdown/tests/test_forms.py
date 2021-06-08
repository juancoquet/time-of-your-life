from django.test import TestCase

from countdown.forms import DOBForm, FUTURE_DOB_ERROR


class DOBFormTest(TestCase):

    def test_future_date_is_not_valid(self):
        form = DOBForm(data={'dob': '2999-12-31'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['dob'], [FUTURE_DOB_ERROR])