from django.core.urlresolvers import resolve
from django.test import TestCase
from django.template.loader import render_to_string
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item, List

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


class ListAndItemModelTest(TestCase):

    def test_saving_and_retreiving_items(self):
        list_ = List()
        list_.save()

        first_text = 'The first ITEM'
        more_text = 'Something else.'

        first_item = Item()
        first_item.text = first_text
        first_item.list = list_
        first_item.save()

        another_item = Item()
        another_item.text = more_text
        another_item.list = list_
        another_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_retreived = saved_items[0]
        another_retreived = saved_items[1]
        self.assertEqual(first_retreived.text, first_text)
        self.assertEqual(first_retreived.list, list_)
        self.assertEqual(another_retreived.text, more_text)
        self.assertEqual(another_retreived.list, list_)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/one-list-to-rule-them-all/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='get coffee', list=list_)
        Item.objects.create(text='get tea', list=list_)

        response = self.client.get('/lists/one-list-to-rule-them-all/')

        self.assertContains(response, 'get coffee')
        self.assertContains(response, 'get tea')


class NewTestList(TestCase):

    def test_block_get(self):
        response = self.client.get('/lists/new')
        self.assertEqual(response.status_code, 405)

    def test_fail_400_bad_request(self):
        response = self.client.post('/lists/new')
        self.assertEqual(response.status_code, 400)

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