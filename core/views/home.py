from rest_framework.views import APIView
from rest_framework.views import Response
from core.models.store import Product
from core.permissions.permissions import IsAuthenticatedOrNot
from core.serializers.store import ProductStoreSerializer
from core.authentications.authenticate import Authentication
from core.models.basket import Basket

from core.authentications.authenticate import generate_token

class Home(APIView) :
    serializer_class = ProductStoreSerializer
    query_set = Product.objects.all()
    def get(self, *args, **kwargs) :
        print(self.request.session)
        print(self.request.session.modified)
        
        print(self.request.session.keys())
        print(self.request.session.values())
        return Response("hello sayed elqasas")
    def post(self, *args, **kwargs) :
        ahmed = self.serializer_class(data = self.request.data)
        if ahmed.is_valid() : ahmed.save()
        else :
            # print(ahmed.error_messages)
            print(ahmed.errors)
        return Response("ahmed from the post")

class Test(APIView) :

    authentication_classes = [Authentication]
    permission_classes =  [IsAuthenticatedOrNot]

    def get(self, *args, **kwargs) :
        print(self.request.user)
        return Response("hello sayed")
    
    def post(self, *args, **kwargs) :

        return Response("hekki sayed")