from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = [ "email","full_name","phone_number","password", "password2"]

        def validate(self, attrs):
            if attrs ['password'] != attrs['password2']:
                raise serializers.ValidationError ("Passswords Do Not Match")

    def create(self, validated_data):
        password = validated_data.pop("password2")
        user = CustomUser.objects.create_user(**validated_data)
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
