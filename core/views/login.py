from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.authentications.authenticate import generate_token


class Login(APIView) :
    
    def post(self, *args, **kwargs) :
        
        data = self.request.data
        email = data.get("email")
        password = data.get("password")

        user = authenticate(username = email, password = password)
        if user:
            return Response(generate_token(user.id))
        return Response(status=status.HTTP_401_UNAUTHORIZED)
