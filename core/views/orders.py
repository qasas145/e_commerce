from core.models.basket import Basket
from core.models.orders import Order, OrderItem
from core.serializers.orders import OrderSerializer
from core.authentications.authenticate import Authentication

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class OrderView(APIView) :

    serializer_class = OrderSerializer
    query_set = Order.objects.all()
    authentication_classes = [Authentication]
        
    def post(self, *args, **kwargs) :

        basket = Basket(self.request)
        order_key = self.request.data.get("order_key")
        user_id = self.request.user.id
        baskettotal = basket.get_total_price()
        self.request.data.pop("user")
        data = self.request.data

        if not Order.objects.filter(order_key = order_key).exists() :

            order = Order.objects.create(user_id = user_id, full_name=data.get("full_name"), address1=data.get("address1"),
                                address2=data.get("address2"), total_paid=baskettotal, order_key=order_key)
            
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])
        
        return Response(OrderSerializer(order).data,status=status.HTTP_201_CREATED)

class UserOrdersView(APIView) :

    serializer_class = OrderSerializer

    def get(self, *args, **kwargs) :

        user = self.request.user
        orders = Order.objects.filter(user = user).filter(billing_status = True)
        return Response(OrderSerializer(orders).data)



class PaymentConfirmation(APIView):

    def post(self, args, **kwargs) :

        data = self.request.data
        Order.objects.filter(order_key=data['data']).update(billing_status=True)
        return Response(status=status.HTTP_200_OK)


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)
