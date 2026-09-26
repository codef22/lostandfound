from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    render,
    redirect
)
from core.models import Item
from core.forms import ItemForm
from core.workflows import can_transition, can_create_claim


@login_required
def create_item(request):
    if request.method == "POST":
        form = ItemForm(
            request.POST,
            request.FILES
        )
        print(request.POST)
        print(request.FILES)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            messages.success(
                request,
                "آیتم به موفقیت ایجاد شد."
            )
            return redirect(
                "item_detail",
                pk=item.id
            )
        else:
            print(form.errors)
            # print("-" * 10)
            # print(form.non_field_errors())
    else:
        form = ItemForm()

    return render(
        request,
        "items/create.html",
        {"form": form}
    )


def list_items(request):
    items = Item.objects.all()

    query = request.GET.get("q")
    status = request.GET.get("status")
    category = request.GET.get("category")

    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query) 
        )
 
    if status:
        items = items.filter(status=status)

    if category:
        items = items.filter(category_id=category)

    return render(
        request,
        "items/item_list.html",
        {"items": items}
    )


@login_required
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


@login_required
def update_item(request, pk):
    print(request.user.get_all_permissions())
    if not request.user.has_perm("core.change_item"):
        return redirect(
            "list_item"
        )
    item = get_object_or_404(
        Item,
        id=pk,
        created_by=request.user
    )
    if request.method == "POST":
        form = ItemForm(
            request.POST,
            request.FILES,
            instance=item
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"آیتم {item.title} با موفقیت ویرایش شد."
            )
            return redirect(
                "item_detail",
                pk=item.id
            )
    else:
        form = ItemForm(instance=item)

    return render(
        request,
        "items/update.html",
        {"form": form}
    )


@login_required
def delete_item(request, pk):
    item = get_object_or_404(
        Item,
        id=pk,
        created_by=request.user
    )
    if request.method == "POST":
        item_title = item.title
        item.delete()
        messages.success(
            request,
            f"آیتم {item_title} با موفقیت حذف شد."
        )
        return redirect("list_item")

    return render(
        request,
        "items/confirm_delete.html",
        {"item": item}
    )


@login_required
def change_status(request, pk):

    new_status = request.POST.get("status")
    
    item = get_object_or_404(
        Item,
        id=pk,
        created_by=request.user
    )
    # guard clause
    if not can_transition(item, new_status):
        messages.error(
            request,
            f"این تغییر وضعیت ممکن نیست."
        )
        return redirect(
            "item_detail",
            pk=item.id
        )
        
    item.status = new_status
    item.save()

    messages.success(
        request,
        f"آیتم به وضعیت {new_status} تغییر یافت."
    )
    
    return redirect(
        "item_detail",
        pk=item.id
    )


@login_required
def create_claim(request, pk):
    # form
    # validiate
    item = get_object_or_404(
        Item,
        id=pk,
    )
    if not can_create_claim(item, request.user):
        messages.error(
            request,
            f"ثبت درخواست برای این آیتم امکان پذیر نیست."
        )
        return redirect(
            "item_detail",
            pk=item.id
        )
