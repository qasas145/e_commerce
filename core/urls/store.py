
from django.urls import path
from core.views.store import *
from django.conf import settings
from django.conf.urls.static import static


app_name = "store"

urlpatterns = [
    path("product/", ProductAll.as_view()),
    path("category/", CategoryList.as_view()),
    path("<slug:slug>/", ProductDetailPk.as_view(), name="product_detail"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
