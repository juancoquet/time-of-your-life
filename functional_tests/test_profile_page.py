from .base import FunctionalTest

from accounts.forms import EVENT_OUT_OF_RANGE_ERROR


class ProfilePageTest(FunctionalTest):

    def test_profile_page(self):
        self.create_user_and_sign_in()

        # At the dashboard, the user sees their current week
        week = self.browser.find_element_by_css_selector(
            '.week.present').get_attribute('id')
        # The user clicks on their profile name
        self.browser.find_element_by_css_selector('.profile').click()

        # They are taken to their profile page, where they can edit their info
        heading = self.browser.find_element_by_tag_name('h2').text
        self.assertEqual(heading, 'My information')

        # They decide to edit all their details realising they made a mistake during sign up
        self.submit_user_update_form(
            email='other@email.com',
            dob='2000-12-01',
            name='Test Name'
        )

        # After submitting the form, the page refreshes and they see a message to tell them
        # it was successful.
        self.assertEqual(self.browser.find_element_by_css_selector(
            '.message').text, 'Success!')

        # They go back to their dashboard and see that the current week has changed.
        self.browser.find_element_by_id('home').click()
        new_week = self.browser.find_element_by_css_selector(
            '.week.present').get_attribute('id')
        self.assertNotEqual(week, new_week)

        # They add a new life event
        self.add_life_event(
            event_name='test event',
            event_date='2005-04-29'
        )

        self.assertEqual(
            len(self.browser.find_elements_by_css_selector('.week.event')), 1)

        # They go back to their profile page, and try to change their DoB to a date that would
        # render their new event out of bounds of their life calendar. They are met with an error.
        self.browser.find_element_by_css_selector('.profile').click()
        self.submit_user_update_form(
            email='other@email.com',
            dob='2006-12-01',
            name='Test Name'
        )
        error = self.browser.find_element_by_id('errors_dob').text
        self.assertEqual(EVENT_OUT_OF_RANGE_ERROR, error)
