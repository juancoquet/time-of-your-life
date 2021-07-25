from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep

from .base import FunctionalTest
from countdown.forms import FUTURE_DOB_ERROR, PAST_DOB_ERROR, DUPLICATE_EVENT_ERROR


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

        # They try to add a duplicate event, but they see an error.
        submit_button = self.browser.find_element_by_name(
            'add_event_btn')
        submit_button.click()

        dupe_error = self.browser.find_element_by_css_selector('.error').text
        self.assertEqual(dupe_error, DUPLICATE_EVENT_ERROR)

        # They hover over the new highlighted event, which reveals a tooltip with information.
        event = self.browser.find_element_by_css_selector('.week.event')
        self.actions.move_to_element(event).perform()
        self.browser.find_element_by_css_selector('.tooltip')

        # They click the visible edit button inside the tooltip and it takes them to a page
        # where they can update the event information.
        edit = self.browser.find_element_by_css_selector('.edit')
        self.actions.move_to_element(
            event).move_to_element(edit).click().perform()

        sleep(4)
        update = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Edit', update)
        event_name_input = self.browser.find_element_by_id('id_event_name')
        event_date_input = self.browser.find_element_by_id('id_event_date')

        # They edit the event info, and are taken back to the calendar page.
        event_name_input.clear()
        event_name_input.send_keys('edited event')
        event_date_input.clear()
        event_date_input.send_keys('2004-03-29')
        self.browser.find_element_by_css_selector('.button-submit').click()

        heading = self.browser.find_element_by_tag_name('h2').text
        self.assertEqual(heading, 'Your Life Calendar')

        # They decide to add another event, in the future this time.
        event_name_input = self.browser.find_element_by_id('id_event_name')
        event_date_input = self.browser.find_element_by_id('id_event_date')
        submit_button = self.browser.find_element_by_name(
            'add_event_btn')

        event_name_input.send_keys('test event')
        event_date_input.send_keys('2078-05-29')
        submit_button.click()

        # The page refreshes and they can now see two highlighted events.
        events = self.browser.find_elements_by_css_selector('.event')
        self.assertEqual(len(events), 2)

    def test_delete_event(self):
        ### Set up ####
        self.browser.find_element_by_id('id_signup').click()
        self.fill_signup_form(
            username='testuser',
            email='test@user.com',
            dob='1995-12-01',
            password='testpass123'
        )
        username_input = self.browser.find_element_by_id('id_login')
        password_input = self.browser.find_element_by_id('id_password')
        username_input.send_keys('test@user.com')
        password_input.send_keys('testpass123')
        self.browser.find_element_by_css_selector('.btn-login').click()
        event_name_input = self.browser.find_element_by_id('id_event_name')
        event_date_input = self.browser.find_element_by_id('id_event_date')
        submit_button = self.browser.find_element_by_name(
            'add_event_btn')

        event_name_input.send_keys('test event')
        event_date_input.send_keys('1998-04-12')
        submit_button.click()

        ############
        ### Test ###
        ############

        # The user decides to delete the event by hovering over the highlighted week
        # and selecting the 'delete' option.
        event = self.browser.find_element_by_css_selector('.week.event')
        self.actions.move_to_element(event).perform()

        delete = self.browser.find_element_by_css_selector('.delete')
        self.actions.move_to_element(
            event).move_to_element(delete).click().perform()

        # They are taken to a new page, asking them to confirm the deletion.
        sleep(4)
        heading = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Delete', heading)

        # They click the delete button to confirm, and are taken back to the dashboard.
        self.browser.find_element_by_css_selector(
            '.btn.button-delete').click()
        heading = self.browser.find_element_by_tag_name('h2').text
        self.assertEqual('Your Life Calendar', heading)

        # The deleted event no longer appears.
        events = self.browser.find_elements_by_css_selector('.week.event')
        self.assertEqual(len(events), 0)
