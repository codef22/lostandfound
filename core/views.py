from django.shortcuts import (
    get_object_or_404,
    render,
    redirect
)
from core.models import Item
from core.forms import ItemForm


def create_item(requests):
    if requests.method == "POST":
        form = ItemForm(requests.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = requests.user
            item.save()
    else:
        form = ItemForm()

    return render(
        requests,
        "items/create.html",
        {"form": form}
    )


def list_items(requests):
    items = Item.objects.all()
    
    return render(
        requests,
        "items/item_list.html",
        {"items": items}
    )


def item_detail(requests, pk):
 
    item = get_object_or_404(
        Item,
        id=pk,
        created_by=requests.user
    )

    return render(
        requests,
        "items/item_detail.html",
        {"item": item}
    )


def update_item(requests, pk):
    item = get_object_or_404(
        Item,
        id=pk,
        created_by=requests.user
    )
    if requests.method == "POST":
        form = ItemForm(
            requests.POST,
            instance=item
        )
        if form.is_valid():
            form.save()
            return redirect(
                "item_detail",
                pk=item.id
            )
    else:
        form = ItemForm(instance=item)

    return render(
        requests,
        "items/update.html",
        {"form": form}
    )


def delete_item(requests, pk):
    item = get_object_or_404(
        Item,
        id=pk,
        created_by=requests.user
    )
    if requests.method == "POST":
        item.delete()
        return redirect("list_item")

    return render(
        requests,
        "items/confirm_delete.html",
        {"item": item}
    )
