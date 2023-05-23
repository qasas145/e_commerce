import json

from core.models.user import Address
from core.models.basket import Basket
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from core.models.orders import Order, OrderItem
from core.models.checkout import DeliveryOptions
from core.serializers.user import AdressSerializer
from core.serializers.checkout import DeliveryOptionsSerializer


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status




# /************************ My Part***************************

class DevliveryChoices(APIView) :

    serializer_class = DeliveryOptionsSerializer

    def get(self, request) :

        deliveryoptions = DeliveryOptions.objects.filter(is_active=True)

        return Response(self.serializer_class(deliveryoptions, many = True).data)



class BasketUpdateDevlivery(APIView) :

    def post(self, request) :

        basket = Basket(request)
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price)

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True

        response = {"total": updated_total_price, "delivery_price": delivery_type.delivery_price}

        return Response(response)



class DevliveryAddress(APIView) :

    serializer_class = AdressSerializer

    def get(self, *args, **kwargs) :
        session = self.request.session
        if "purchase" not in self.request.session:
            messages.success(self.request, "Please select delivery option")
            return Response(self.request.META["HTTP_REFERER"])

        addresses = Address.objects.filter(customer=self.request.user).order_by("-default")

        if "address" not in self.request.session:
            session["address"] = {"address_id": str(addresses[0].id)}
        else:
            session["address"]["address_id"] = str(addresses[0].id)
            session.modified = True

        return Response(self.serializer_class(addresses, many = True).data)
    
class PaymentSelection(APIView) :

    def get(self, request) :

        session = request.session
        if "address" not in request.session:
            messages.success(request, "Please select address option")
            return Response(request.META["HTTP_REFERER"])

        return Response({})


####
# PayPay
####
from paypalcheckoutsdk.orders import OrdersGetRequest

from core.views.paypal import PayPalClient


class PaymentComplete(APIView) :
    def get(self, request) :
        PPClient = PayPalClient()

        body = request.data
        data = body["orderID"]
        user_id = request.user.id

        requestorder = OrdersGetRequest(data)
        response = PPClient.client.execute(requestorder)

        total_paid = response.result.purchase_units[0].amount.value

        basket = Basket(request)
        order = Order.objects.create(
            user_id=user_id,
            full_name=response.result.purchase_units[0].shipping.name.full_name,
            email=response.result.payer.email_address,
            address1=response.result.purchase_units[0].shipping.address.address_line_1,
            address2=response.result.purchase_units[0].shipping.address.admin_area_2,
            postal_code=response.result.purchase_units[0].shipping.address.postal_code,
            country_code=response.result.purchase_units[0].shipping.address.country_code,
            total_paid=response.result.purchase_units[0].amount.value,
            order_key=response.result.id,
            payment_option="paypal",
            billing_status=True,
        )
        order_id = order.pk

        for item in basket:
            OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])

        return Response("Payment completed!", status=status.HTTP_200_OK)



class PaymentSuccessful(APIView) :

    def get(self, request) :

        basket = Basket(request)
        basket.clear()
        return Response({})



# /*****************************************************


