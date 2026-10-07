from django.contrib import messages
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    render,
    redirect
)
from core.models import Item
from core.forms import ItemForm


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

    date_from = request.GET.get("date_from") 
    date_to = request.GET.get("date_to")

    sort = request.GET.get("sort")

    # جستجو
    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query) 
        )

    # فیلتر وضعیت
    if status:
        items = items.filter(status=status)

    # فیلتر دسته‌بندی
    if category:
        items = items.filter(category_id=category)

    # فیلتر از تاریخ 
    if date_from: 
        items = items.filter(event_date__gte=date_from) 

    # فیلتر تا تاریخ 
    if date_to: 
        items = items.filter(event_date__lte=date_to)

    # مرتب‌سازی 
    sort_options = { 
        "newest": "-created_at", 
        "oldest": "created_at", 
    } 
    
    sort_field = sort_options.get(sort, "-created_at") 
    
    items = items.order_by(sort_field)

    # تعداد نتایج بعد از Search و Filter 
    result_count = items.count()

    return render(
        request,
        "items/item_list.html",
        {
            "items": items,
            "result_count": result_count,
        }
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


def update_item(request, pk):
    item = get_object_or_404(
        Item,
        id=pk,
        created_by=request.user
    )
    if request.method == "POST":
        form = ItemForm(
            request.POST,
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
