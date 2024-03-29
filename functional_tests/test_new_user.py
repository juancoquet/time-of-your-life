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
            'Create an account'
        )

        # They see a form with the fields username, email, date of birth and password.
        # They try to sign up with a date of birth in the future, but they are shown an error.
        self.submit_signup_form(
            username='testuser',
            email='test@user.com',
            day='01',
            month='12',
            year='2100',
            password='testpass123'
        )
        self.assertIn(FUTURE_DOB_ERROR, self.browser.page_source)

        # They try to sign up with a date of birth too far in the past, and once again see an error.
        self.submit_signup_form(
            username='testuser',
            email='test@user.com',
            day='01',
            month='12',
            year='1901',
            password='testpass123'
        )
        self.assertIn(PAST_DOB_ERROR, self.browser.page_source)

        # They enter valid details, and are logged in to their new account.
        self.submit_signup_form(
            username='testuser',
            email='test@user.com',
            day='01',
            month='12',
            year='1995',
            password='testpass123'
        )
        self.assertIn('grid/dashboard/', self.browser.current_url)

        # Once logged in, they see the nav bar has changed.
        # The can see that they are logged in.
        logged_in_as = self.browser.find_element_by_id('id_logged_in').text
        self.assertEqual(logged_in_as, 'testuser')

        # They also see that the Sign up and Log In elements have disappeared.
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('id_login_link')
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('id_signup')

        # They see an option to log out
        self.browser.find_element_by_id('id_logout')

        # On their dashboard page, they see their life calendar and a form to add life events.
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
        self.add_life_event(
            event_name='test event',
            day='12',
            month='04',
            year='1998'
        )

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
        self.add_life_event(
            event_name='test event',
            day='12',
            month='04',
            year='1998'
        )

        dupe_error = self.browser.find_element_by_css_selector('.error').text
        self.assertEqual(dupe_error, DUPLICATE_EVENT_ERROR)

        # They hover over the new highlighted event, which reveals a tooltip with information.
        event = self.browser.find_element_by_css_selector('.week.event')
        self.actions.move_to_element(event).perform()
        self.browser.find_element_by_css_selector('.tooltip')

        # They click the visible edit button inside the tooltip and it takes them to a page
        # where they can update the event information.
        sleep(2)
        edit = self.browser.find_elements_by_css_selector('.tooltip__link')[0]
        self.actions.move_to_element(
            event).move_to_element(edit).click().perform()

        sleep(2)
        update = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Edit', update)
        event_name_input = self.browser.find_element_by_id('id_event_name')
        day_input = self.browser.find_element_by_id('id_day')
        month_input = self.browser.find_element_by_id('id_month')
        year_input = self.browser.find_element_by_id('id_year')

        # They edit the event info, and are taken back to the calendar page.
        event_name_input.clear()
        event_name_input.send_keys('edited event')
        day_input.clear()
        month_input.clear()
        year_input.clear()
        day_input.send_keys('29')
        month_input.send_keys('03')
        year_input.send_keys('2004')
        self.browser.find_element_by_css_selector('.button-submit').click()

        heading = self.browser.find_element_by_css_selector(
            '.container__heading--left').text
        self.assertEqual(heading, 'Your Life Calendar')

        # They decide to add another event, in the future this time.
        self.add_life_event(
            event_name='test event',
            day='29',
            month='05',
            year='2078'
        )

        # The page refreshes and they can now see two highlighted events.
        events = self.browser.find_elements_by_css_selector('.event')
        self.assertEqual(len(events), 2)

        # They decide they've seen enough, and log out of their account.
        self.browser.find_element_by_id('id_logout').click()
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('id_logged_in')

    def test_delete_event(self):
        ### Set up ####
        self.create_user_and_sign_in()

        self.add_life_event(
            event_name='test event',
            day='12',
            month='04',
            year='1998'
        )

        ############
        ### Test ###
        ############

        # The user decides to delete the event by hovering over the highlighted week
        # and selecting the 'delete' option.
        event = self.browser.find_element_by_css_selector('.week.event')
        self.actions.move_to_element(event).perform()

        sleep(2)
        delete = self.browser.find_elements_by_css_selector('.tooltip__link')[
            1]
        self.actions.move_to_element(
            event).move_to_element(delete).click().perform()

        # They are taken to a new page, asking them to confirm the deletion.
        sleep(2)
        heading = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Delete', heading)

        # They click the delete button to confirm, and are taken back to the dashboard.
        self.browser.find_element_by_css_selector(
            '.btn.button-delete').click()
        heading = self.browser.find_element_by_css_selector(
            '.container__heading--left').text
        self.assertEqual('Your Life Calendar', heading)

        # The deleted event no longer appears.
        events = self.browser.find_elements_by_css_selector('.week.event')
        self.assertEqual(len(events), 0)
