import random
from rest_framework.response import Response
from account.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from account.models import User
from rest_framework import status, generics

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save() # This will call the custom create method and not save it to the database

            userreg_serializer = RegSerializer(user) # serialize the user object

            return Response({
                "user": userreg_serializer.data,
                "msg": "OTP code was sent to your email successfully."
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def verify_otp(otp_code, user):
    # Retrieve the expected OTP code from the user model
    expected_otp_code = user.otp

    # Compare the provided OTP code with the expected OTP code
    if str(otp_code) == str(expected_otp_code):
        return True
    else:
        return False


class OTPVerificationView(APIView):
    def post(self, request, format=None):
        otp_code = request.data.get('otp_code')
        user_id = request.data.get('user_id')

        if not otp_code or not user_id:
            return Response({"message": "Invalid OTP verification data."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "Invalid user ID."}, status=status.HTTP_400_BAD_REQUEST)

        # Perform OTP verification here using your chosen method
        if not verify_otp(otp_code, user):
            return Response({"message": "Invalid OTP code."}, status=status.HTTP_400_BAD_REQUEST)

        # Set the user's is_verified attribute to True
        user.is_verified = True
        user.save()

        return Response({"message": f"Registration completed successfully. Welcome {user.first_name}"}, status=status.HTTP_200_OK)


class LoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email').lower()
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            userlog_serializer = UserLogSerializer(user) 
            
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({"user": userlog_serializer.data ,"token":token, "msg": f"Welcome {user.first_name}"}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": {"non_field_errors":["Email or password is not valid"]}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)