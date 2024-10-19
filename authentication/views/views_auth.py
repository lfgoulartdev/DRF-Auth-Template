"""
API views for authentication app auth features.
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

user = get_user_model()


class RegisterView(APIView):
    """
    Register a new user.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Register a new user.
        """
        data = request.data

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")

        if username is None or email is None or password is None:
            return Response(
                {"message": "Please provide both email and password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.objects.filter(email=email).exists():
            return Response(
                {"message": "User already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        return Response(
            {"message": "User created successfully."},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    Login a user.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Login a user.
        """
        data = request.data

        email = data.get("email")
        password = data.get("password")

        if email is None or password is None:
            return Response(
                {"message": "Please provide both email and password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_obj = user.objects.filter(email=email).first()

        if user_obj is None:
            return Response(
                {"message": "User does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user_obj.check_password(password):
            return Response(
                {"message": "Invalid password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, _ = Token.objects.get_or_create(user=user_obj)

        return Response(
            {"message": "Login successful.", "token": token.key},
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """
    Logout a user.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Logout a user.
        """
        request.user.auth_token.delete()

        return Response(
            {"message": "Logout successful."},
            status=status.HTTP_200_OK,
        )
