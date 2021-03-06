from django.shortcuts import render, redirect, get_object_or_404

from lists.models import List
from lists.forms import ExistingListItemForm, ItemForm


def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = get_object_or_404(List, id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)

    return render(request, 'lists/list.html', context={
        'list': list_,
        'form': form,
    })


def new_list(request):
    if request.method != 'POST':
        form = ItemForm()
        return render(request, 'lists/home.html', context={'form': form})

    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)

    else:
        return render(request, 'lists/home.html', context={
            'form': form,
        })
