import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_get_it_later(self):
        # Go to our super-sweet to-do list-app
        self.browser.get('http://localhost:8000')

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
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1. get peanut butters' for row in rows)
        )

        # Add another item is presented to the user. This time: 'put butters', return..

        # Page updates, both items showing.

        # The app will tell the user that the URL changes to reflect the uniqueness of
        # the list

        # Going to that URL, the list is still there.

        ...
        self.fail('To-do...')

if __name__ == '__main__':
    #unittest.main(warnings='ignore')
    unittest.main()
