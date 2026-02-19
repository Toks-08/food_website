from django.shortcuts import render
from .serializers import RegisterSerializer, LoginSerializer
from .models import CustomUser
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token as authtoken
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class RegistrationView(CreateAPIView):
    model = CustomUser
    serializer_class = RegisterSerializer
    permission_classes=[AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "Message":"User Created Succcessfully",
                "email":user.email,
            }, status=status.HTTP_201_CREATED
        )
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created= authtoken.objects.get_or_create(user=user)
        return Response (
            {
                "Message":"Login Successful",
                "token":token.key,
                "user":{
                    'id':user.id,
                    'email':user.email,
                }
            }, status=status.HTTP_200_OK
        )