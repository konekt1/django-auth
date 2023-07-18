from django.urls import path
from account.views import UserRegistrationView, UserLoginView, UserProfileView, OTPVerificationView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path('verify-otp/', OTPVerificationView.as_view(), name='otp-verification'),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
]