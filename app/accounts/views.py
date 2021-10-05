from rest_framework import generics, status, permissions
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenViewBase

from .models import UserAccount
from .serializers import (
    UserSerializer, CreateUserAccountSerializer
)


class UserList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer


class CreateUser(generics.CreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = CreateUserAccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        #  serializer for create access token
        token_serializer = TokenObtainPairSerializer(
            data={'email': serializer.validated_data['email'], 'password': request.data['password']})
        token_serializer.is_valid(raise_exception=True)
        # logic for combine data
        serializer_data = serializer.data
        serializer_data.update(token_serializer.validated_data)

        headers = self.get_success_headers(serializer_data)
        return Response(serializer_data, status=status.HTTP_201_CREATED, headers=headers)


class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer


@parser_classes((FormParser, MultiPartParser))
class UserCurrent(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(pk=self.request.user.uuid)
        self.check_object_permissions(self.request, obj)
        return obj


class UserLogout(generics.RetrieveAPIView):
    """
    An Api View which provides a method to logout from current account
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenViewBase):
    serializer_class = TokenObtainPairSerializer
