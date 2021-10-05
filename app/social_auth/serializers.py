from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import UserAccount
from . import google, facebook
from .register import register_social_user


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            email = user_data['email']
        except:
            raise serializers.ValidationError('The token is invalid or expired. Please login again.')

        provider = settings.FACEBOOK_AUTH_PROVIDER
        return register_social_user(provider=provider, email=email)


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError('The token is invalid or expired. Please login again.')

        if user_data['aud'] != settings.SOCIAL_AUTH_GOOGLE_OAUTH2_CLIENT_ID:
            raise AuthenticationFailed('oops, who are you?')

        if not user_data['email_verified']:
            raise AuthenticationFailed('verify your email first')

        email = user_data['email']
        provider = settings.GOOGLE_AUTH_PROVIDER

        return register_social_user(provider=provider, email=email)
