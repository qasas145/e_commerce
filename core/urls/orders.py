from django.urls import path
from core.views.orders import OrderView
from django.conf import settings
from django.conf.urls.static import static

app_name = "orders"
urlpatterns = [
    path("order/", OrderView.as_view()),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
