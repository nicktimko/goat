import sys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        '''Short-circuit setting up our own server if we're doing it live.'''
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        # RAGNAROK INVOKED
        self.browser.refresh() # shut up Windows
        self.browser.quit()

    def assertRowsInTable(self, expected_texts):
        return self._assertRowsInTable(expected_texts)

    def assertRowsNotInTable(self, expected_texts):
        return self._assertRowsInTable(expected_texts, negate=True)

    def _assertRowsInTable(self, expected_texts, negate=False):
        method = self.assertNotIn if negate else self.assertIn
        table = self.browser.find_element_by_id('id_list_table')
        row_text = [row.text for row in table.find_elements_by_tag_name('tr')]
        for expected in expected_texts:
            method(expected, row_text)

    def add_new_item(self, keys):
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(keys)
