from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep

from .base import FunctionalTest
from countdown.forms import FUTURE_DOB_ERROR, PAST_DOB_ERROR


class NewUserTest(FunctionalTest):

    def test_new_user_signup(self):
        # A new visitor visits the site. They see a button inviting them to sign up.
        sign_up = self.browser.find_element_by_id('id_signup')

        # They click the button, and they are taken to a sign up page.
        sign_up.click()
        self.assertEqual(
            self.browser.find_element_by_tag_name('h2').text,
            'Sign up'
        )

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

        # They enter valid details, and are redirected to the login page.
        self.fill_signup_form(
            username='testuser',
            email='test@user.com',
            dob='1995-12-01',
            password='testpass123'
        )
        self.assertIn('accounts/login/', self.browser.current_url)

        # They enter their email and password and are redirected to their profile page.
        username_input = self.browser.find_element_by_id('id_login')
        password_input = self.browser.find_element_by_id('id_password')
        username_input.send_keys('test@user.com')
        password_input.send_keys('testpass123')
        self.browser.find_element_by_css_selector('.btn-login').click()

        self.assertIn('grid/dashboard/', self.browser.current_url)

        # Once logged in, they see the nav bar has changed.
        # The can see that they are logged in.
        logged_in_as = self.browser.find_element_by_id('id_logged_in').text
        self.assertEqual(logged_in_as, 'Logged in as testuser')

        # They also see that the Sign up and Log In elements have disappeared.
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('id_login_link')
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('id_signup')

        # They see an option to log out
        self.browser.find_element_by_id('id_logout')

        # On their profile page, they see their life calendar and a form to add life events.
        past_weeks = self.browser.find_elements_by_css_selector('.week.past')
        future_weeks = self.browser.find_elements_by_css_selector(
            '.week.future')
        present_week = self.browser.find_elements_by_css_selector(
            '.week.present')
        self.assertGreater(len(past_weeks), 1)
        self.assertGreater(len(future_weeks), 1)
        self.assertEqual(len(present_week), 1)
        all_weeks = self.browser.find_elements_by_css_selector('.week')
        self.assertEqual(len(all_weeks), 52*90)

        self.browser.find_element_by_name('add_event')

        # They use the event form to add a life event. The page refreshes, and the event
        # is shown on the calendar.
        event_name_input = self.browser.find_element_by_id('id_event_name')
        event_date_input = self.browser.find_element_by_id('id_event_date')
        submit_button = self.browser.find_element_by_name(
            'add_event_btn')

        event_name_input.send_keys('test event')
        event_date_input.send_keys('1998-04-12')
        submit_button.click()

        past_weeks = self.browser.find_elements_by_css_selector('.week.past')
        future_weeks = self.browser.find_elements_by_css_selector(
            '.week.future')
        present_week = self.browser.find_elements_by_css_selector(
            '.week.present')
        event_week = self.browser.find_elements_by_css_selector('.week.event')
        self.assertGreater(len(past_weeks), 1)
        self.assertGreater(len(future_weeks), 1)
        self.assertEqual(len(present_week), 1)
        self.assertEqual(len(event_week), 1)
        all_weeks = self.browser.find_elements_by_css_selector('.week')
        self.assertEqual(len(all_weeks), 52*90)

        # They hover over the new highlighted event, which reveals a tooltip with information.
        event = self.browser.find_element_by_css_selector('.week.event')
        self.actions.move_to_element(event).perform()
        self.browser.find_element_by_css_selector('.tooltip')

        # They click the visible edit button inside the tooltip and it takes them to a page
        # where they can update the event information.
        edit = self.browser.find_element_by_css_selector('.edit')
        self.actions.move_to_element(
            event).move_to_element(edit).click().perform()

        sleep(2)
        update = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Edit', update)
        event_name_input = self.browser.find_element_by_id('id_event_name')
        event_date_input = self.browser.find_element_by_id('id_event_date')

        # TODO: Test add multiple events

        # TODO: Test home redirects to dashboard
