from django import forms
from django.forms import ModelForm, ValidationError

from core.models import Item, Claim

from django.utils import timezone


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = [
            "title",
            "description",
            "location",
            "event_date",
            "category",
            "status"
        
        ]
    def clean_event_date(self):
        event_date = self.cleaned_data["event_date"]
        today = timezone.localdate()

        if event_date > today:
            raise forms.ValidationError(
                "تاریخ رویداد نمی‌تواند در آینده باشد. "
                "لطفاً تاریخ امروز یا یک تاریخ گذشته را وارد کنید."
            )

        return event_date
    
    def clean_description(self):
        description = self.cleaned_data["description"]

        if len(description) < 20:
            raise ValidationError(
                "توضیحات وارد شده نباید کمتر از ۲۰ کارکتر باشد"
            )

        return description

    def clean_title(self):
        title = self.cleaned_data["title"]

        if len(title) < 3:
            raise ValidationError(
                "عنوان خیلی کوتاه است. یک عنوان مناسب همانند <کیف پول مشکی> ثبت کنید."
            )

        return title
    
    def clean_title(self):
        title = self.cleaned_data["title"].strip()

        general_words = [
            "وسیله",
            "چیز",
            "گمشده",
        ]

        if title in general_words:
            raise forms.ValidationError(
                "عنوان واردشده خیلی عمومی است. "
                "لطفاً عنوان دقیق‌تری مانند «کیف مدرسه مشکی» وارد کنید."
            )

        return title


class ClaimForm(ModelForm):
    class Meta:
        model = Claim
        fields = [
            "proof_text",
        ]
