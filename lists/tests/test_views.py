from unittest import skip

from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils.html import escape

from lists.views import home_page
from lists.models import Item, List
from lists.forms import (
    ExistingListItemForm,
    ItemForm,
    DUPLICATE_ITEM_ERROR,
    EMPTY_ITEM_ERROR,
    ITEM_FORM_FIELD_TEXT,
)

class ViewTestCase(TestCase):

    def post_item(self, text='', url_args=None, no_data=False):
        if url_args is None:
            url_args = []

        if no_data:
            data = {}
        else:
            data = {
                ITEM_FORM_FIELD_TEXT: text,
            }

        return self.client.post(
            self.url(*url_args),
            data=data,
        )


class HomePageTest(ViewTestCase):

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(ViewTestCase):

    def url(self, id):
        return reverse('view_list', args=[str(id)])

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(self.url(list_.id))
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_items_for_corresponding_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='get coffee', list=correct_list)
        Item.objects.create(text='get tea', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='get cheese', list=other_list)
        Item.objects.create(text='get milk', list=other_list)

        response = self.client.get(self.url(correct_list.id))

        self.assertContains(response, 'get coffee')
        self.assertContains(response, 'get tea')
        self.assertNotContains(response, 'get cheese')
        self.assertNotContains(response, 'get milk')

    def test_passes_correect_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        another_list = List.objects.create()

        response = self.client.get(self.url(correct_list.id))

        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_post_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        another_list = List.objects.create()

        self.post_item('New item!', [correct_list.id])

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'New item!')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        another_list = List.objects.create()

        response = self.post_item('New item!', [correct_list.id])

        self.assertRedirects(response, self.url(correct_list.id))

    def test_invalid_input_displays_error(self):
        response = self.post_item('', [List.objects.create().id])
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_invalid_input_renders_list_template(self):
        response = self.post_item('', [List.objects.create().id])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_invalid_input_includes_form(self):
        response = self.post_item('', [List.objects.create().id])
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_invalid_items_not_saved(self):
        self.post_item('', [List.objects.create().id])
        self.assertEqual(Item.objects.count(), 0)

    def test_list_shows_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(self.url(list_.id))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def cause_duplicate(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_, text='Bread')
        response = self.post_item('Bread', [list_.id])
        return response

    def test_duplicate_error_displays_error(self):
        response = self.cause_duplicate()
        self.assertContains(response, escape(DUPLICATE_ITEM_ERROR))

    def test_duplicate_error_returns_to_list(self):
        response = self.cause_duplicate()
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_duplicate_not_saved(self):
        response = self.cause_duplicate()
        self.assertEqual(1, Item.objects.count())


class NewListTest(ViewTestCase):

    def url(self):
        return reverse('new_list')

    def test_get_redirect_to_home(self):
        response = self.client.get(self.url())
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_get_shows_no_error(self):
        response = self.client.get(self.url())
        self.assertNotContains(response, escape(EMPTY_ITEM_ERROR))

    def test_fail_bad_request_redirects_to_home(self):
        response = self.post_item(no_data=True)
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_after_bad_request_form_still_there(self):
        response = self.post_item(no_data=True)
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_saving_a_post(self):
        my_item = 'Some to-do item'
        response = self.post_item(my_item)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, my_item)

    def test_redirects_after_post(self):
        response = self.post_item('asdf')

        list_ = List.objects.first()
        self.assertRedirects(response, reverse('view_list', args=[list_.id]))

    def test_invalid_input_renders_home_template(self):
        response = self.post_item('')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_invalid_input_shows_error_on_home(self):
        response = self.post_item('')

        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)

    def test_after_invalid_input_form_still_there(self):
        response = self.post_item('')

        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_items_not_saved(self):
        self.post_item('')

        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
