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
        

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_items_for_corresponding_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='get coffee', list=correct_list)
        Item.objects.create(text='get tea', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='get cheese', list=other_list)
        Item.objects.create(text='get milk', list=other_list)

        response = self.client.get('/lists/{}/'.format(correct_list.id))

        self.assertContains(response, 'get coffee')
        self.assertContains(response, 'get tea')
        self.assertNotContains(response, 'get cheese')
        self.assertNotContains(response, 'get milk')

    def test_passes_correect_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        another_list = List.objects.create()

        response = self.client.get('/lists/{}/'.format(correct_list.id))

        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):

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
        list_ = List.objects.first()
        self.assertRedirects(response, '/lists/{}/'.format(list_.id))


class NewItemTest(TestCase):

    def test_can_save_a_post_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        another_list = List.objects.create()

        self.client.post(
            '/lists/{}/add_item'.format(correct_list.id),
            data={'item_text': 'New item!'},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'New item!')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        another_list = List.objects.create()

        response = self.client.post(
            '/lists/{}/add_item'.format(correct_list.id),
            data={'item_text': 'New item!'},
        )

        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))