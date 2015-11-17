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

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, my_item)

    def test_home_page_redirects_after_post(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'asdf'

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

        # self.assertIn(my_item, response.content.decode(encoding='utf-8'))
        # expected_html = render_to_string(
        #     'lists/home.html',
        #     {'new_item_text': my_item}
        # )
        # self.assertEqual(
        #     response.content.decode(encoding='utf-8'),
        #     expected_html
        # )

    def test_home_page_displays_multiple_items(self):
        Item.objects.create(text='item1')
        Item.objects.create(text='item2')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('item1', response.content.decode())
        self.assertIn('item2', response.content.decode())

    def test_home_page_only_saves_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):

    def test_saving_and_retreiving_items(self):
        first_text = 'The first ITEM'
        more_text = 'Something else.'

        first_item = Item()
        first_item.text = first_text
        first_item.save()

        another_item = Item()
        another_item.text = more_text
        another_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_retreived = saved_items[0]
        another_retreived = saved_items[1]
        self.assertEqual(first_retreived.text, first_text)
        self.assertEqual(another_retreived.text, more_text)
