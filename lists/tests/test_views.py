from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils.html import escape

from ..views import home_page
from ..models import Item, List
from ..forms import ItemForm, ITEM_FORM_FIELD_TEXT


class HomePageTest(TestCase):

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


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

    def test_can_save_a_post_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        another_list = List.objects.create()

        self.client.post(
            '/lists/{}/'.format(correct_list.id),
            data={ITEM_FORM_FIELD_TEXT: 'New item!'},
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
            '/lists/{}/'.format(correct_list.id),
            data={ITEM_FORM_FIELD_TEXT: 'New item!'},
        )

        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()

        response = self.client.post(
            '/lists/{}/'.format(list_.id),
            data={ITEM_FORM_FIELD_TEXT: ''},
        )

        expected_error = escape("You can't have an empty list item!")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertContains(response, expected_error)

    def test_invalid_items_not_saved(self):
        list_ = List.objects.create()

        self.client.post(
            '/lists/{}/'.format(list_.id),
            data={ITEM_FORM_FIELD_TEXT: ''},
        )

        self.assertEqual(Item.objects.filter(list=list_.id).count(), 0)


class NewListTest(TestCase):

    def test_block_get(self):
        response = self.client.get('/lists/new')

        self.assertEqual(response.status_code, 405)

    def test_get_redirect_to_home(self):
        response = self.client.get('/lists/new')

        self.assertTemplateUsed(response, 'lists/home.html')

    def test_fail_400_bad_request(self):
        response = self.client.post('/lists/new')

        self.assertEqual(response.status_code, 400)

    def test_fail_bad_request_redirects_to_home(self):
        response = self.client.post('/lists/new')

        self.assertTemplateUsed(response, 'lists/home.html')
        expected_error = escape("Bad request.")
        self.assertContains(response, expected_error, status_code=400)

    def test_saving_a_post(self):
        my_item = 'Some to-do item'

        self.client.post(
            '/lists/new',
            data={
                ITEM_FORM_FIELD_TEXT: my_item,
            },
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, my_item)

    def test_redirects_after_post(self):
        response = self.client.post(
            '/lists/new',
            data={
                ITEM_FORM_FIELD_TEXT: 'asdf',
            },
        )
        list_ = List.objects.first()
        self.assertRedirects(response, '/lists/{}/'.format(list_.id))

    def test_validation_errors_are_sent_back_to_home_page(self):
        response = self.client.post('/lists/new', data={
            ITEM_FORM_FIELD_TEXT: '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')
        expected_error = escape("You can't have an empty list item!")
        self.assertContains(response, expected_error)

    def test_invalid_items_not_saved(self):
        self.client.post('/lists/new', data={ITEM_FORM_FIELD_TEXT: ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
