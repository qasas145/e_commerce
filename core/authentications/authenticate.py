from rest_framework.authentication import BaseAuthentication
from rest_framework import HTTP_HEADER_ENCODING
import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from core.models.user import CustomUser
from datetime import datetime, timedelta



class Authentication(BaseAuthentication) :
    def authenticate(self, request):
        return self.verify_authentication(request)

    def authenticate_header(self, request):
        return super().authenticate_header(request)

    
    def get_header_authorization(self, request) :
        auth = request.META.get("HTTP_AUTHORIZATION", b'')
        if isinstance(auth, str) :
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth


    def verify_authentication(self, request) :
        auth = self.get_header_authorization(request=request)
        if not auth :
            return (None, None)
        token = auth.decode("utf-8").split(" ")[1]
        decoded_token = self.decode_token(token) 
        user = get_object_or_404(CustomUser, pk=decoded_token['user_id']) if decoded_token else None
        return (user,decoded_token)

    def decode_token(self, token) :
        try :
            token = jwt.decode(token, key=settings.JWT_KEY, algorithms="HS256")
            return token
        except (jwt.DecodeError, jwt.ExpiredSignatureError) :
            return None
    
def generate_token(user_id) :
    token = jwt.encode(payload={
        "user_id" : user_id,
        'exp' : datetime.utcnow()+timedelta(minutes=1),
    },
    algorithm="HS256",
    key=settings.JWT_KEY,
    )
    return token

