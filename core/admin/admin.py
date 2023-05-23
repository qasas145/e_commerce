from django.contrib import admin
from core.models.user import CustomUser
from core.models.orders import Order, OrderItem
from core.models.store import Category

admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(Category)
