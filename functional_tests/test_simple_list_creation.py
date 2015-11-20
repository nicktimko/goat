from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_get_it_later(self):
        # Edith goes to our super-sweet to-do list-app
        self.browser.get(self.server_url)

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

        # When return is hit, take the user to a new URL and display
        # the item in a list.
        inputbox.send_keys(Keys.ENTER)
        ediths_list_url = self.browser.current_url
        self.assertRegex(ediths_list_url, '/lists/.+')
        self.assertRowsInTable([
            '1. get peanut butters',
        ])

        # Add another item is presented to the user.
        # This time: 'put butters', return..
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('put butters')
        inputbox.send_keys(Keys.ENTER)

        # Page updates, both items showing.
        self.assertRowsInTable([
            '1. get peanut butters',
            '2. put butters',
        ])

        ## remove session from browser
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # frank visits app, expects a clear list (not edith's stuff)
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('get peanut butters', page_text)
        self.assertNotIn('put butters', page_text)

        # frank starts a list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('brew coffee')
        inputbox.send_keys(Keys.ENTER)

        # frank gets his URL
        franks_list_url = self.browser.current_url
        self.assertRegex(franks_list_url, '/lists/.+')
        self.assertNotEqual(franks_list_url, ediths_list_url)

        # still nothing from edith shows up
        self.assertRowsNotInTable([
            '1. get peanut butters',
            '2. put butters',
        ])
        self.assertRowsInTable([
            '1. brew coffee'
        ])

        # satisfied, they both invoke ragnarok.
