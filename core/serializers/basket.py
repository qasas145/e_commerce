from rest_framework import serializers
from .store import ProductStoreSerializer
from django.shortcuts import get_list_or_404
from core.models.store import Product

class BasketSerializer(serializers.Serializer) :
    product_id = serializers.IntegerField()
    qty = serializers.IntegerField()
    