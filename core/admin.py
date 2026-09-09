from django.contrib import admin
from core.models import Category, Item, Claim


admin.site.register(Category)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "status",
        "created_at"
    )
    list_filter = (
        "status",
        "category"
    )
    search_fields = (
        "title",
        "description"
    )
    ordering = (
        "-created_at",
    )


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "item",
        "claimant",
        "status",
        "created_at"
    )
    list_filter = (
        "status",
    )

    ordering = (
        "-created_at",
    )
