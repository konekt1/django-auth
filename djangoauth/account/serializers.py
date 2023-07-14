from xml.dom import ValidationErr
from django.forms import ValidationError
from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'current_location', 'intern_category']


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number", "current_location", "intern_category", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.pop("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Password and confirm Password don't match")

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user
    
class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name']

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ["email","password"]