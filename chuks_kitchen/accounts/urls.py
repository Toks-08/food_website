from django.urls import path
from .views import RegistrationView, LoginView,VerifyOTPView

urlpatterns = [
    path("signup/", RegistrationView.as_view(), name='register' ),
    path('login/', LoginView.as_view(), name ="login"),
    path('verify/', VerifyOTPView.as_view(), name='verify-otp')
]