import hashlib

from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import Item, List


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(
            list_.get_absolute_url(),
            '/lists/{}/'.format(list_.id)
        )


class ItemModelTest(TestCase):

    def test_useful_string_repr(self):
        item = Item(text='Hello!')
        self.assertEqual(
            str(item),
            'Hello!'
        )

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')


class ListAndItemModelTest(TestCase):

    def test_item_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_cannot_save_duplicates(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='Hello')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='Hello')
            item.full_clean()

    def test_can_save_duplicates_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='Hello')
        item = Item(list=list2, text='Hello')
        item.full_clean()

    def test_list_ordering(self):
        list_ = List.objects.create()

        def md5(x):
            return hashlib.md5(bytes([x])).hexdigest()
        items = [
            Item.objects.create(list=list_, text=md5(i))
            for i
            in range(10)
        ]

        self.assertEqual(list(Item.objects.all()), items)
