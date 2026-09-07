from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=100)


class Item(models.Model):

    class Status(models.TextChoices):
        OPEN = "open", "باز"
        REVIEWING = "reviewing", "در حال بررسی"
        DELIVERED = "delivered", "تحویل داده شده"
        CLOSED = "closed", "بسته شده"

    title = models.CharField(max_length=128)
    description = models.TextField()
    location = models.CharField(max_length=200)
    event_date = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Claim(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار بررسی"
        APPROVED = "approved", "تایید شده"
        REJECTED = "rejected", "رد شده"

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    claimant = models.ForeignKey(User, on_delete=models.CASCADE)
    proof_text = models.TextField(help_text="چیزی بنویسید که مالکیت شما را ثابت کند.")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
