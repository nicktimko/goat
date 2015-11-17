from django.core.urlresolvers import resolve
from django.test import TestCase
from django.template.loader import render_to_string
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('lists/home.html')
        self.assertEqual(
            response.content.decode(encoding='utf-8'),
            expected_html
        )

    def test_home_page_can_save_post_request(self):
        my_item = 'Some to-do item'

        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = my_item

        response = home_page(request)

        self.assertIn(my_item, response.content.decode(encoding='utf-8'))
        expected_html = render_to_string(
            'lists/home.html',
            {'new_item_text': my_item}
        )
        self.assertEqual(
            response.content.decode(encoding='utf-8'),
            expected_html
        )

class ItemModelTest(TestCase):

    def test_saving_and_retreiving_items(self):
        first_item = Item()
        first_item.text = 'The first ITEM'
        first_item.save()

        another_item = Item()
        another_item.text = 'Something else.'
        another_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_retreived = saved_items[0]
        another_retreived = saved_items[1]
        self.assertEqual(first_retreived.text, 'The first ITEM')
        self.assertEqual(another_retreived.text, 'Something else.')
