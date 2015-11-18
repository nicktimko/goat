from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from lists.models import Item, List

# Create your views here.
def home_page(request):
    return render(request, 'lists/home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html', context={
        'items': items,
    })

@require_http_methods(['POST'])
def new_list(request):
    try:
        item_text = request.POST['item_text']
    except KeyError:
        return HttpResponseBadRequest()

    list_ = List.objects.create()
    Item.objects.create(text=item_text, list=list_)
    return redirect('/lists/one-list-to-rule-them-all/')
