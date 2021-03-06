from django.test import TestCase

from lists.forms import (
    ItemForm,
    ExistingListItemForm,
    EMPTY_ITEM_ERROR,
    DUPLICATE_ITEM_ERROR,
)
from lists.models import List, Item


class ItemFormTest(TestCase):

    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validates_blank_lines(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_saving_to_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'hello!'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'hello!')
        self.assertEqual(new_item.list, list_)


class ExistingItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validates_blank_lines(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validates_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='Coffee')
        form = ExistingListItemForm(for_list=list_, data={'text': 'Coffee'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'Tea'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.first())
