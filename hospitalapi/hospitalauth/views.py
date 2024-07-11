from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from hospitalauth.serializers import UserRegistrationSerializer, UserLoginSerializer, HospitalUserListSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from .models import HospitalUser

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class HospitalUserRegitrationView(APIView):

# {
#     "name": "Akhtaruzzaman Khan",
#     "email": "akhtar@gmail.com",
#     "address": "39939 Stevenson Common",
#     "date_of_birth": "18 September 1997",
#     "phone_number": "555555555",
#     "password": "123",
#     "password2": "123"
# }
    
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registered Succesfully'})

class UserListView(generics.ListAPIView):
    queryset = HospitalUser.objects.all()
    serializer_class = HospitalUserListSerializer
    
class HospitalUserLoginView(APIView):
    
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            user = authenticate(email=email, password=password)
            if user:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Successfull'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'User Is Not Valid'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

