from django.contrib.auth import authenticate
from accounts.models import UserAccount
import os
from rest_framework.exceptions import AuthenticationFailed


def register_social_user(provider, email):
    filtered_user_by_email = UserAccount.objects.filter(email=email).first()

    if filtered_user_by_email:

        if provider == filtered_user_by_email.auth_provider:

            registered_user = authenticate(
                email=email, password=os.environ.get('SOCIAL_SECRET'))

            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email.auth_provider)

    else:
        user = { 'email': email, 'password': os.environ.get('SOCIAL_SECRET')}
        user = UserAccount.objects.create_user(**user)
        user.auth_provider = provider
        user.save()

        new_user = authenticate(
            email=email, password=os.environ.get('SOCIAL_SECRET'))
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }