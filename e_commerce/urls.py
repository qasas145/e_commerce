from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("orders/", include('core.urls.orders')),
    path("user/", include('core.urls.user')),
    path("store/", include('core.urls.store')),
    path("basket/", include('core.urls.basket')),
    path("checkout/", include('core.urls.checkout')),
    path("authentication/", include("core.urls.authentication"))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
