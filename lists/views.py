from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from lists.models import Item, List


def home_page(request):
    return render(request, 'lists/home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'lists/list.html', context={
        'list': list_,
    })


@require_http_methods(['POST'])
def new_list(request):
    try:
        item_text = request.POST['item_text']
    except KeyError:
        return HttpResponseBadRequest()

    list_ = List.objects.create()
    Item.objects.create(text=item_text, list=list_)
    return redirect('/lists/{}/'.format(list_.id))


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    item_text = request.POST['item_text']
    Item.objects.create(
        text=item_text,
        list=list_,
    )

    return redirect('/lists/{}/'.format(list_.id))
