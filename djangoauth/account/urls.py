from django.urls import path
from account.views import RegistrationView, LoginView, ProfileView, OTPVerificationView

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path('verify-otp/', OTPVerificationView.as_view(), name='otp-verification'),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
]