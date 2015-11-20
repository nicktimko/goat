from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_enter_blank_items(self):
        # Hillary visits the webpage and accidentally tries to submit an
        # empty item.
        self.browser.get(self.server_url)
        self.add_new_item('\n')

        # The webpage refreshes and has an error message stating the
        # list does not accept blank items
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item!")

        # Resigned, she enters some text and submits it
        self.add_new_item('Get coffee\n')
        self.assertRowsInTable(['1. Get coffee'])

        # Absentmindedly, she attempts to enter another blank item
        self.add_new_item('\n')

        # And still the server rejects the error with a visible error message.
        self.assertRowsInTable(['1. Get coffee'])
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item!")

        # But in correcting the error, it works once again works
        self.add_new_item('Get RED BULLLLL\n')
        self.assertRowsInTable(['1. Get coffee', '2. Get RED BULLLLL'])
