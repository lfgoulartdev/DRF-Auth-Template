"""
URL configuration for authentication app.
"""

from django.urls import path
from authentication.views.views_auth import RegisterView, LoginView, LogoutView


urlpatterns = [
    path("api/v1/auth/register/", RegisterView.as_view(), name="register"),
    path("api/v1/auth/login/", LoginView.as_view(), name="login"),
    path("api/v1/auth/logout/", LogoutView.as_view(), name="logout"),
]
