from unittest import skip

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    @skip
    def test_cannot_enter_blank_items(self):
        # Hillary visits the webpage and accidentally tries to submit an
        # empty item.
        self.browser.get(self.server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(Keys.ENTER)

        # The webpage refreshes and has an error message stating the
        # list does not accept blank items
        #self.browser.find_element

        # Resigned, she enters some text and submits it
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('get coffee')
        inputbox.send_keys(Keys.ENTER)

        # Absentmindedly, she attempts to enter another blank item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(Keys.ENTER)

        # And still the server rejects the error with a visible error message.

        # But in correcting the error, it works once again works
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('get RED BULLLLL')
        inputbox.send_keys(Keys.ENTER)

        self.fail('TODO: Finish me.')
