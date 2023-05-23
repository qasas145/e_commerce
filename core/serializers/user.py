from rest_framework import serializers
from core.models.user import CustomUser, Address


class UserSerializer(serializers.Serializer) :
    email = serializers.EmailField(max_length = 20)
    password = serializers.CharField()

class FullUserSerializer(serializers.ModelSerializer) :
    class Meta :
        model = CustomUser
        exclude = ("country",)

class AdressSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Address
        fields = "__all__"


class ActiviationSerializer(serializers.Serializer) :
    uuid = serializers.UUIDField()
    token = serializers.CharField()
    