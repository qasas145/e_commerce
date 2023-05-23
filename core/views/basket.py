from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from core.models.basket import Basket
from core.models.store import Product
from core.serializers.basket import BasketSerializer
from django.shortcuts import get_object_or_404


class BasketView(APIView) :

    serializer_class = BasketSerializer
    
    def get(self, *args, **kwargs) :
        query_set = Basket(self.request)
        return Response(query_set.all())
    
    def post(self, *args, **kwargs) :
        query_set = Basket(self.request)
        print(query_set)
        id = self.request.data.get("product_id", None)
        print(id)
        if not id :
            return Response("hello sayed")
        product = get_object_or_404(Product, pk = int(id))
        qty = int(self.request.data.get("qty"))
        query_set.add(product, qty)
        # return Response(self.serializer_class(self.query_set, many=True).data)
        return Response("hello sayed elqasas")

    


class BasketPkView(APIView) :
    serializer_class = BasketSerializer
    def put(self, *args, **kwargs) :
        query_set = Basket(self.request)
        id = kwargs.get("id", None)
        product = get_object_or_404(Product, id)
        qty = int(kwargs.get("qty"))
        query_set.update(product, qty)
        return Response(self.serializer_class(self.query_set, many=True).data)
        
    def delete(self, *args, **kwargs) :
        query_set = Basket(self.request)
        id = kwargs.get("id", None)
        product = get_object_or_404(Product, id)
        query_set.delete(product)