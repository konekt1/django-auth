
from rest_framework import serializers
from account.models import User
from django.contrib.auth import get_user_model


User = get_user_model()

class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'current_location', 'intern_category']

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User  # Update to your CustomUser model
        fields = ["email", "first_name", "last_name", "phone_number", "current_location", "intern_category", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }


    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.pop("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Password and confirm Password don't match")

        attrs["confirm_password"] = confirm_password  # Add confirm_password back to attrs

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        confirm_password = validated_data.pop("confirm_password")

        user = User.objects.create_user(**validated_data)  # Use create_user method
        user.set_password(password)
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
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'current_location', 'intern_category']