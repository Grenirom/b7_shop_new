from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import generics, permissions
from apps.account.serializers import RegisterSerializer, LogOutSerialzer

User = get_user_model()


class UserRegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny, ]


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny, )


class RefreshView(TokenRefreshView):
    permission_classes = (AllowAny, )


class LogoutView(APIView):
    serializer_class = LogOutSerialzer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response('Успешно вышли с аккаунта', 200)
