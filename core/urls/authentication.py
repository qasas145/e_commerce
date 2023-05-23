from django.urls import path
from core.views.login import Login

app_name = "authentication"

urlpatterns = [
    path("login/", Login.as_view())
] 
