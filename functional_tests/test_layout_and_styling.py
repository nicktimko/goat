# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # shelly goes to the homepage
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # she notices that the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=20
        )

        # input on the add-an-item page is also good
        inputbox.send_keys('buy beer\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=20
        )
