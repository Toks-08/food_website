from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUser, Referral, EmailOTP
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    referral_code = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = CustomUser
        fields = [ "email","full_name","phone_number","password", "password2","referral_code"]

    def validate(self, attrs):
        if attrs ['password'] != attrs['password2']:
            raise serializers.ValidationError ("Passswords Do Not Match")
        return attrs
        
    def validate_referral_code(self, value):
        try:
            referral = Referral.objects.get(code=value)
            if not referral.is_valid():
                raise serializers.ValidationError("Referral code expired or inactive")
        except Referral.DoesNotExist:
            raise serializers.ValidationError("Invalid referral code")
        return value
        

    def create(self, validated_data):
        password = validated_data.pop("password2")
        referral_obj = validated_data.pop("referral_code", None)
        user = CustomUser.objects.create_user(**validated_data)
        if referral_obj:
            user.referral_used = referral_obj
            user.save()
            
        return user
   

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, validated_data):
        user = authenticate(**validated_data)
        if not user:
            raise serializers.ValidationError("Invalid Username Or Password")
        validated_data['user']=user
        return validated_data
    

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6, min_length=6)

    def validate(self, data):
        email = data.get('email')
        otp_code = data.get('otp')

        try:
            user = CustomUser.objects.get(email=email)
            # Get the latest OTP for this user
            otp_obj = EmailOTP.objects.filter(user=user, otp=otp_code).latest('created_at')
            
            # Check 1: Is it already verified?
            if otp_obj.is_verified:
                raise serializers.ValidationError("This OTP has already been used.")

            # Check 2: Use model logic to check if it's expired
            if otp_obj.is_expired():
                raise serializers.ValidationError("This OTP has expired. Please request a new one.")

            # Check 3: Brute force protection
            if otp_obj.attempts >= 5:
                raise serializers.ValidationError("Too many failed attempts. Request a new code.")

            data['otp_instance'] = otp_obj
            data['user'] = user
            return data

        except (CustomUser.DoesNotExist, EmailOTP.DoesNotExist):
            raise serializers.ValidationError("Invalid email or OTP code.")
