import json
import os
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models.basket import Basket
from .orders import payment_confirmation


class OrderPlaced(APIView) :

    def get(self, *args, **kwargs) :

        request = self.request
        basket = Basket(request)
        basket.clear()
        return Response(request)

class BasketView1(APIView):
    def get(self, *args,**kwargs):
        request = self.request
        basket = Basket(request)
        total = str(basket.get_total_price())
        total = total.replace('.', '')
        total = int(total)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency='gbp',
            metadata={'userid': request.user.id}
        )
        data = {'client_secret': intent.client_secret, 
                                                            'STRIPE_PUBLISHABLE_KEY': os.environ.get('STRIPE_PUBLISHABLE_KEY')}
        return Response(data=data, status=status.HTTP_200_OK)
'''
class StripeWebhook(APIView) :
    def get(self, *args, **kwargs) :
        request = self.request
        payload = request.body
        event = None

        try:
            event = stripe.Event.construct_from(
                json.loads(payload), stripe.api_key
            )
        except ValueError as e :
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Handle the event
        if event.type == 'payment_intent.succeeded':
            
            payment_confirmation(event.data.object.client_secret)
            

        else:
            print('Unhandled event type {}'.format(event.type))

        return Response(status=status.HTTP_200_OK)
'''