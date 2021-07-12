from .base import FunctionalTest
from countdown.forms import FUTURE_DOB_ERROR, PAST_DOB_ERROR


class NewUserTest(FunctionalTest):

    def test_new_user_signup(self):
        # A new visitor visits the site. They see a button inviting them to sign up.
        sign_up = self.browser.find_element_by_id('sign-up')

        # They click the button, and they are taken to a sign up page.
        sign_up.click()
        self.assertEqual(
            self.browser.find_element_by_tag_name('h2').text,
            'Sign up'
        )

        # TODO: Test errors are raised with invalid input
        # They see a form with the fields username, email, date of birth and password.
        # They try to sign up with a date of birth in the future, but they are shown an error.
        self.fill_signup_form(
            username='testuser',
            email='test@user.com',
            dob='2100-12-01',
            password='testpass123'
        )
        self.assertIn(FUTURE_DOB_ERROR, self.browser.page_source)

        # They try to sign up with a date of birth too far in the past, and once again see an error.
        self.fill_signup_form(
            username='testuser',
            email='test@user.com',
            dob='1901-12-01',
            password='testpass123'
        )
        self.assertIn(PAST_DOB_ERROR, self.browser.page_source)
        # TODO: Test signup with no username
        # TODO: Test signup with no email
        # TODO: Test signup with invalid email
        # TODO: Test signup with no dob
        # TODO: Test successful signup attempt
