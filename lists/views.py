from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .models import Item, List
from .forms import ItemForm, ITEM_FORM_FIELD_TEXT

EMPTY_LIST_ERROR = "You can't have an empty list item!"

def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(
                text=request.POST[ITEM_FORM_FIELD_TEXT],
                list=list_,
            )
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = EMPTY_LIST_ERROR

    items = Item.objects.filter(list=list_)
    return render(request, 'lists/list.html', context={
        'list': list_,
        'error': error,
    })


def new_list(request):
    # if request.method != 'POST':
    #     return render(request, 'lists/home.html', status=405, context={})

    form = ItemForm(data=request.POST)

    item_text = request.POST[ITEM_FORM_FIELD_TEXT]
    # try:
    #     item_text = request.POST[ITEM_FORM_FIELD_TEXT]
    # except KeyError:
    #     return render(request, 'lists/home.html', status=400, context={
    #         'form': form
    #     })

    if form.is_valid():
        list_ = List.objects.create()
        item = Item.objects.create(text=item_text, list=list_)
        return redirect(list_)

    else:
        return render(request, 'lists/home.html', context={
            'form': form,
        })
