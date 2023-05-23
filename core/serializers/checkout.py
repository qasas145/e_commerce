from core.models.checkout import DeliveryOptions
from rest_framework import serializers



class DeliveryOptionsSerializer(serializers.ModelSerializer) :
    class Meta :
        model = DeliveryOptions
        fields = "__all__"