from datetime import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)
        self.browser.get(self.live_server_url)

    def tearDown(self):
        if self._test_has_failed():
            for i, handle in enumerate(self.browser.window_handles):
                self.browser.switch_to.window(handle)
                filepath = self._create_error_capture_filepath(i)
                timestamp = datetime.now()
                self.browser.save_screenshot(f'{filepath}/screenshot-{timestamp}.png')
                self.capture_html(filepath, timestamp)
        self.browser.quit()

    def _test_has_failed(self):
        # returns True if any errors were raised during test run
        return any(error for (method, error) in self._outcome.errors)

    def _create_error_capture_filepath(self, handle_index):
        timestamp = datetime.now()
        classname = self.__class__.__name__
        method = self._testMethodName
        dir_path = f'functional_tests/error_capture/{timestamp}-{classname}.{method}/{handle_index}'
        os.makedirs(dir_path)
        return dir_path

    def capture_html(self, filepath, timestamp):
        filename = f'{filepath}/source-{timestamp}.html'
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.errorlist')