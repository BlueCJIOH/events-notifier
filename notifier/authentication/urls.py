from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import UserRegister

urlpatterns = [
    path("auth/sign-in/", TokenObtainPairView.as_view(), name="sign-in"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/sign-up/", UserRegister.as_view(), name="sign-up"),
]
