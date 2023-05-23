from rest_framework import serializers
from core.models.orders import Order

class OrderSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Order
        fields = "__all__"