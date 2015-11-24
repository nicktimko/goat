from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item!"
DUPLICATE_ITEM_ERROR = "You already have that in your list!"

ITEM_FORM_FIELD_TEXT = 'text'


class ItemForm(forms.models.ModelForm):

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            })
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }


class ExistingListItemForm(ItemForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    # class Meta(ItemForm.Meta):
    #     error_messages = {
    #         'text': {'required': EMPTY_ITEM_ERROR},
    #         '__all__': {
    #             'unique_together': DUPLICATE_ITEM_ERROR,
    #         }
    #     }

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            # ?!? private method?
            # maybe: https://docs.djangoproject.com/en/1.8/topics/forms/modelforms/#validation-on-a-modelform # noqa
            self._update_errors(e)

    def save(self):
        return forms.models.ModelForm.save(self)
