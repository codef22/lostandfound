from django.shortcuts import render

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
