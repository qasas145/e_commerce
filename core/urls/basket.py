from django.urls import path
from core.views.basket import BasketPkView, BasketView
from django.conf import settings
from django.conf.urls.static import static

app_name = "basket"

urlpatterns = [
    path("basket/", BasketView.as_view()),
    path("basket/<int:id>/", BasketPkView.as_view()),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
