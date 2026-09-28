from django.forms import ModelForm, ValidationError

from core.models import Item, Claim


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = [
            "title",
            "description",
            "location",
            "event_date",
            "category",
            "status",
            "image"
        ]
    
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


class ClaimForm(ModelForm):
    class Meta:
        model = Claim
        fields = [
            "proof_text",
        ]
