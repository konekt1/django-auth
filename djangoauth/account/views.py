from rest_framework.response import Response
from account.serializers import UserRegistrationSerializer, UserRegSerializer, UserLogSerializer, UserLoginSerializer 
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)

            userreg_serializer = UserRegSerializer(user)  # serialize the user object

            return Response({
                "user": userreg_serializer.data,
                "token": token,
                "msg": "Registration Successful"
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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