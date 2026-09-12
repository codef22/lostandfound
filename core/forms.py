from django.forms import ModelForm, ValidationError

from core.models import Item


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
    
    def clean_description(self):
        description = self.cleaned_data["description"]

        if len(description) < 20:
            raise ValidationError(
                "توضیحات وارد شده نباید کمتر از ۲۰ کارکتر باشد"
            )

        return description

    def clean(self):
        clean_data = super().clean()

        event_date = clean_data["event_date"]
        status = clean_data["status"]

        if status == Item.Status.DELIVERED and event_date is None:
            raise ValidationError(
                "برای وضعیت تحویل داده شده تاریخ نمیتواند خالی باشد."
                )

        return clean_data

