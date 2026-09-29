from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    render,
    redirect
)
from core.models import Item, Claim
from core.forms import ItemForm, ClaimForm
from core.workflows import can_transition, can_create_claim


@login_required
def create_item(request):
    if request.method == "POST":
        form = ItemForm(
            request.POST,
        )
        print(request.POST)
        
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
    all_items_exist = Item.objects.exists()
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

    if not all_items_exist:
        empty_state = "no_items"
    elif not items.exists():
        empty_state = "no_results"
    else:
        empty_state = None

    return render(
        request,
        "items/item_list.html",
        {
            "items": items,
            "empty_state": empty_state,
        }
    )


@login_required
def item_detail(requests, pk):
 
    item = get_object_or_404(
        Item,
        id=pk
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
def submit_claim(request, pk):
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
    if request.method == "POST":
        form = ClaimForm(request.POST)

        if form.is_valid():
            claim = form.save(commit=False)

            claim.item = item
            claim.claimant = request.user
            claim.status = Claim.Status.PENDING
            claim.save()

            messages.success(
                request,
                "درخواست مالکیت شما ثبت شد."
            )
            return redirect(
                "item_detail",
                pk=item.id
            )

    else:
        form = ClaimForm()

    return render(
        request,
        "items/submit_claim.html",
        {
            "form": form,
            "item": item
        }
    )


@login_required
def claim_review_list(request):

    claims = Claim.objects.filter(
        status=Claim.Status.PENDING
    ).order_by("created_at")

    return render(
        request,
        "claim/review_list.html",
        {"claims": claims}
    )


@login_required
def approve_reject_claim(request, pk):
 
    claim = get_object_or_404(
        Claim,
        id=pk
    )
    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status == 'approve':
            claim.status = Claim.Status.APPROVED
            claim.item.status = Item.Status.REVIEWING
            claim.item.save()
            claim.save()
            msg_txt = "درخواست مالکیت تایید شد."
        elif new_status == 'reject':
            claim.status = Claim.Status.REJECTED
            claim.save()
            msg_txt = "درخواست مالکیت رد شد."
        else:
            msg_txt = "درخواست مالیکت وضعیت درستی ندارد."

        messages.success(
            request,
            msg_txt
        )

    return redirect("claim_review_list")