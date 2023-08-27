
from rest_framework import serializers
from account.models import User
from django.contrib.auth import get_user_model


User = get_user_model()

class RegSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'first_name', 'last_name', 'role']


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, style={"input_type": "password"})
    class Meta:
        model = User
        fields = ["email", "password", "confirm_password", "first_name", "last_name", "role"]
        extra_kwargs = {
            "password": {"write_only": True}
        }


    def create(self, validated_data):
        password = validated_data.pop("password")
        confirm_password = validated_data.pop("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Password and confirm Password don't match")

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

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

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', "role"]