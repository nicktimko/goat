from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def assertRowsInTable(self, table, expected_texts):
        row_text = [row.text for row in table.find_elements_by_tag_name('tr')]
        for expected in expected_texts:
            self.assertIn(expected, row_text)

    def test_can_start_a_list_and_get_it_later(self):
        # Go to our super-sweet to-do list-app
        self.browser.get(self.live_server_url)

        # it screams "TO-DO" in a heading
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Check title for bookmarking
        self.assertIn('To-Do', self.browser.title)

        # Prompt to enter a new item immediately
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Types: 'get peanut butters' (I'm hungry)
        inputbox.send_keys('get peanut butters')

        # When return is hit, update the page and put the item into a list.
        inputbox.send_keys(Keys.ENTER)
        table = self.browser.find_element_by_id('id_list_table')
        self.assertRowsInTable(table, [
            '1. get peanut butters',
        ])

        # Add another item is presented to the user.
        # This time: 'put butters', return..
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('put butters')
        inputbox.send_keys(Keys.ENTER)

        # Page updates, both items showing.
        table = self.browser.find_element_by_id('id_list_table')
        self.assertRowsInTable(table, [
            '1. get peanut butters',
            '2. put butters',
        ])

        # The app will tell the user that the URL changes to reflect the
        # uniqueness of the list

        # Going to that URL, the list is still there.

        ...
        self.fail('Written tests passing, but there is more to-do...')
