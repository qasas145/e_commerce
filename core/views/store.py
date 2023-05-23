from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models.store import Category, Product
from core.serializers.store import ProductStoreSerializer, CategoryStoreSerailizer


class ProductAll(APIView) :
    serializer_class = ProductStoreSerializer
    query_set = Product.objects.all()
    def get(self, *args, **kwargs) :
        products = Product.objects.prefetch_related("product_image").filter(is_active=True)
        return Response(self.serializer_class(products).data)

class ProductDetailPk(APIView) :

    serializer_class = ProductStoreSerializer

    def get(self, *args, **kwargs) :
        
        product = get_object_or_404(Product, slug=kwargs.get("slug"), is_active=True)

        return Response(self.serializer_class(product).data)

class CategoryList(APIView) :
    serializer_class = CategoryStoreSerailizer
    query_set = Category.objects.all()
    def get(self, *args, **kwargs) :
        category_slug = self.data.get("category_slug")
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True)
        )
        return Response(self.serializer_class(category).data)


