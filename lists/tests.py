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


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/one-list-to-rule-them-all/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='get coffee')
        Item.objects.create(text='get tea')

        response = self.client.get('/lists/one-list-to-rule-them-all/')

        self.assertContains(response, 'get coffee')
        self.assertContains(response, 'get tea')


class NewTestList(TestCase):

    def test_saving_a_post(self):
        my_item = 'Some to-do item'

        self.client.post(
            '/lists/new',
            data={
                'item_text': my_item,
            },
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, my_item)

    def test_redirects_after_post(self):
        response = self.client.post(
            '/lists/new',
            data={
                'item_text': 'asdf',
            },
        )

        self.assertRedirects(response, '/lists/one-list-to-rule-them-all/')
