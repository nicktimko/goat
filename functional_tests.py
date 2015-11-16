from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_get_it_later(self):
        # Go to our super-sweet to-do list-app
        self.browser.get('http://localhost:8000')

        # Check title for bookmarking
        self.assertIn('To-do', self.browser.title)

        # Prompt to enter a new item immediately

        # Types: 'get peanut butters' (I'm hungry)

        # When return is hit, update the page and put the item into a list.

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
