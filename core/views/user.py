from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.hashers import make_password
from django.utils.encoding import force_bytes, force_text

from core.models.orders import Order
from core.serializers.store import ProductStoreSerializer
from core.views.orders import UserOrdersView
from  core.models.store import Product
from core.models.user import Address
from core.views.tokens import account_activation_token
from core.serializers.orders import OrderSerializer
from core.serializers.user import ActiviationSerializer, AdressSerializer, FullUserSerializer
from core.models.user import CustomUser

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status


# /**********************************************/
# my part ###########################

class WishList(APIView) :
    serializer_class = ProductStoreSerializer

    def get(self, *args, **kwargs) :

        products = Product.objects.filter(users_wishlist=self.request.user)
        return Response(ProductStoreSerializer(products, many = True).data)
    
    def put(self, *args, **kwargs) :

        product = get_object_or_404(Product, id=kwargs.get("id"))
        if product.users_wishlist.filter(id=self.request.user.id).exists():
            product.users_wishlist.remove(self.request.user)
            messages.success(self.request, product.title + " has been removed from your WishList")
        else:
            product.users_wishlist.add(self.request.user)
            messages.success(self.request, "Added " + product.title + " to your WishList")
        return Response(self.request.META["HTTP_REFERER"])
    

class AddressView(ModelViewSet) :
    serializer_class = AdressSerializer
    queryset = Address.objects.all()
    

class AddressViewPk(APIView) :
    serializer_class = AdressSerializer

    def get(self, *args, **kwargs) :
        addresses = Address.objects.filter(customer=self.request.user)
        return Response(self.serializer_class(addresses, many = True).data)


class SetDefualtView(APIView) :
    
    def get(self, *args, **kwargs) :
            
        Address.objects.filter(customer=self.request.user, default=True).update(default=False)
        Address.objects.filter(pk=kwargs.get("id"), customer=self.request.user).update(default=True)

        previous_url = self.request.META.get("HTTP_REFERER")

        if "delivery_address" in previous_url:
            return reverse("checkout:delivery_address")

        return reverse("user:addresses")


class UserView(ModelViewSet) :

    serializer_class = FullUserSerializer
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):

        data = request.data 
        data._mutable = True
        data['password'] = make_password(data.get("password"))
        data['is_active'] = 'false'

        serialized_data = self.serializer_class(data = data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        
        created_user = get_object_or_404(CustomUser, pk = serialized_data.data['id'])

        current_site = get_current_site(request)
        subject = "Activate your Account"

        token = account_activation_token.make_token(created_user)
        uuid_token = urlsafe_base64_encode(force_bytes(created_user.id))
        print(uuid_token)
        print(token)

        message = f"user : {serialized_data.data['first_name']}, domain : {current_site.domain},uuid : {uuid_token}, token : {token}"

        # created_user.email_user(subject=subject, message=message, from_email = "qasas145@gmail.com")


        return Response(serialized_data.data)

class ActivationView(APIView):

    serializer_class = ActiviationSerializer

    def post(self, *args, **kwargs) :
        token = self.request.data.get("token")
        uidb64 = self.request.data.get("uuid")
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(self.request, user)
            return Response("Activated .", status=status.HTTP_201_CREATED)
        else:
            return Response("Not activated .", status=status.HTTP_401_UNAUTHORIZED)

class Dashboard(APIView) :
    def get(self, *args, **kwargs) :
        user_id = self.request.user.id
        orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
        orders_serialized = OrderSerializer(orders, many=True).data
        return Response(orders_serialized)

# /**********************************************/


