
from django.urls import path
from core.views import (
    create_item,
    list_items,
    item_detail,
    update_item,
    delete_item,
    change_status,
    submit_claim,
    claim_review_list,
    approve_reject_claim,
)


urlpatterns = [
    path("", list_items, name="list_item"),
    path("create/", create_item, name="create_item"),
    path("<int:pk>/", item_detail, name='item_detail'),
    path("<int:pk>/edit/", update_item, name="update_item"),
    path("<int:pk>/delete/", delete_item, name="delete_item"),
    path("<int:pk>/change_status/", change_status, name="change_status_item"),
    path("<int:pk>/claim/", submit_claim, name="submit_claim"),
    path("claim_list/", claim_review_list, name="claim_review_list"),
    path("change_claim_status/<int:pk>/", approve_reject_claim, name="approve_reject_claim"),
]
