from rest_framework import serializers
from django.shortcuts import get_list_or_404
from core.models.store import Product, ProductType, Category

class ProductTypeSerializer(serializers.ModelSerializer) :
    class Meta :
        fields = "__all__"
        model = ProductType

class CategoryStoreSerailizer(serializers.ModelSerializer) :
    class Meta :
        fields = "__all__"
        model = Category
class ProductStoreSerializer(serializers.Serializer) :
    class Meta :
        fields = "__all__"
        model = Product