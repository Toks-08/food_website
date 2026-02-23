from django.shortcuts import render
from .serializers import RegisterSerializer, LoginSerializer, VerifyOTPSerializer
from .models import CustomUser, EmailOTP, Referral
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token as authtoken
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
import random

# Create your views here.
class RegistrationView(CreateAPIView):
    model = CustomUser
    serializer_class = RegisterSerializer
    permission_classes=[AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # --- NEW: Generate and Save OTP ---
        otp_code = str(random.randint(100000, 999999))
        EmailOTP.objects.create(
            user=user,
            otp=otp_code,
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        
        # --- NEW: Create a Referral Code for the new user to share ---
        Referral.objects.create(referrer=user)

       # DEBUG: Check your terminal to see the code since we haven't set up a real email server yet
        print(f"DEBUG: OTP for {user.email} is {otp_code}")

        return Response(
            {
                "Message": "User Created Successfully. Please verify your email with the OTP sent.",
                "email": user.email,
            }, status=status.HTTP_201_CREATED
        )
    
    # NEW: The view to handle account activation
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        otp_obj = serializer.validated_data['otp_instance']

        # Activate the user
        user.is_active = True
        user.is_email_verified = True
        user.save()

        # Mark OTP as used
        otp_obj.is_verified = True
        otp_obj.save()

        return Response({"Message": "Account activated! You can now login."}, status=status.HTTP_200_OK)

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