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

    def clean_image(self): 
        image = self.cleaned_data.get("image") 
        if image: 
            max_size = 2 * 1024 * 1024 # 2MB 
            if image.size > max_size: 
                raise ValidationError( "حجم تصویر نباید بیشتر از ۲ مگابایت باشد." 
                ) 
        return image
