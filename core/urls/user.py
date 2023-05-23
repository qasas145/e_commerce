from django.urls import path
from core.views.user import ActivationView, AddressView, AddressViewPk, Dashboard, UserView, WishList
from core.views.home import Test
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

app_name = "user"

router = DefaultRouter()
router.register("user", UserView, "user")
router.register("addresses", AddressView, "view")
urlpatterns = router.urls

urlpatterns = [
    path("home/", Test.as_view()),
    path("dashboard/", Dashboard.as_view()),
    path("activate/", ActivationView.as_view()),
    path("addresses_view/", AddressViewPk.as_view()),
    path("wishlist/", WishList.as_view()),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
