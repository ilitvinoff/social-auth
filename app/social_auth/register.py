from django.conf import settings
from django.contrib.auth import authenticate
from accounts.models import UserAccount
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def register_social_user(provider, email):
    filtered_user_by_email = UserAccount.objects.filter(email=email).first()

    if filtered_user_by_email:

        if provider == filtered_user_by_email.auth_provider:

            registered_user = authenticate(
                email=email, password=settings.PROVIDER_SECRET_KEY_MAP.get(provider))

            return get_tokens_for_user(registered_user)

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email.auth_provider)

    else:
        user = { 'email': email, 'password': settings.PROVIDER_SECRET_KEY_MAP.get(provider), 'auth_provider':provider}
        user = UserAccount.objects.create_user(**user)
        user.save()

        new_user = authenticate(
            email=email, password=settings.PROVIDER_SECRET_KEY_MAP.get(provider))

        return get_tokens_for_user(new_user)