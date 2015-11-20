from django.test import TestCase

from lists.models import Item, List


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
