from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .models import Item, List
from .forms import ItemForm

EMPTY_LIST_ERROR = "You can't have an empty list item!"

def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(
                text=request.POST['item_text'],
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


@require_http_methods(['POST'])
def new_list(request):
    try:
        item_text = request.POST['item_text']
    except KeyError:
        return HttpResponseBadRequest()

    list_ = List.objects.create()
    item = Item.objects.create(text=item_text, list=list_)

    try:
        item.full_clean()
        return redirect(list_)
    except ValidationError:
        list_.delete()
        return render(request, 'lists/home.html', context={
            'error': EMPTY_LIST_ERROR,
        })
