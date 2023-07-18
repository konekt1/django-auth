import random
from rest_framework.response import Response
from account.serializers import UserRegistrationSerializer, UserRegSerializer, UserLogSerializer, UserLoginSerializer, UserProfileSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from account.models import User

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def generate_otp_code():
    # Generate a 6-digit OTP code
    return str(random.randint(100000, 999999))


def send_otp(user_email, otp_code):
    # Send the OTP code via email
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp_code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(serializer.validated_data)  # Do not save the user yet
            user.owner = request.user

            # Generate OTP code and save it to user model
            otp_code = generate_otp_code()
            user.otp = otp_code
            user.save()

            send_otp(user.email, otp_code)

            token = get_tokens_for_user(user)

            userreg_serializer = UserRegSerializer(user)  # serialize the user object

            return Response({
                "user": userreg_serializer.data,
                "token": token,
                "msg": "OTP code was sent to your email successfully."
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def verify_otp(otp_code, user):
    # Retrieve the expected OTP code from the user model
    expected_otp_code = user.otp

    # Compare the provided OTP code with the expected OTP code
    if str(otp_code) == str(expected_otp_code):
        # OTP code is valid, perform additional actions if needed
        user.is_verified = True
        user.save()
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

        # OTP code is valid, perform additional registration steps if needed
        # ...

        # Mark the user as verified
        user.is_verified = True
        user.save()

        return Response({"message": "Registration completed successfully. "f"Welcome {user.first_name}"}, status=status.HTTP_200_OK)


class UserLoginView(APIView):
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
    
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)