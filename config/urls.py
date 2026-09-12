
from django.contrib import admin
from django.urls import path
from core.views import create_item


urlpatterns = [
    path('admin/', admin.site.urls),
    path("item/create/", create_item)
]
