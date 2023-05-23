"""e_commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from core.views.checkout import *
from django.conf import settings
from django.conf.urls.static import static


app_name = "checkout"

urlpatterns = [
    path("delivery_address/", DevliveryAddress.as_view(), name="delivery_address"),
    path("deliverychoices", DevliveryChoices.as_view(), name="deliverychoices"),
    path("basket_update_delivery/", BasketUpdateDevlivery.as_view(), name="basket_update_delivery"),
    path("payment_selection/", PaymentSelection.as_view(), name="payment_selection"),
    path("payment_complete/", PaymentComplete.as_view(), name="payment_complete"),
    path("payment_successful/", PaymentSuccessful.as_view(), name="payment_successful"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
