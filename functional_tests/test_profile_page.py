from .base import FunctionalTest


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

        # They decide to edit their date of birth, realising they made a mistake during sign up
        dob_field = self.browser.find_element_by_id('id_dob')
        dob_field.clear()
        dob_field.send_keys('2000-12-01')
        self.browser.find_element_by_css_selector('.btn.button-submit').click()

        # They go back to their dashboard and see that the current week has changed.
        self.browser.find_element_by_id('home').click()
        new_week = self.browser.find_element_by_css_selector(
            '.week.present').get_attribute('id')
        self.assertNotEqual(week, new_week)

        # TODO: finish profile page tests
