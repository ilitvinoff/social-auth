from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from accounts.managers import CustomUserManager
from core.models import CoreModel


class UserAccount(PermissionsMixin, AbstractBaseUser, CoreModel):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    AUTH_PROVIDERS = {
        settings.FACEBOOK_AUTH_PROVIDER: "facebook",
        settings.GOOGLE_AUTH_PROVIDER: "google",
        settings.EMAIL_AUTH_PROVIDER: "email"
    }

    email = models.EmailField(verbose_name=_('Email'), unique=True)
    is_staff = models.BooleanField(verbose_name=_('is admin'), default=False)
    is_active = models.BooleanField(verbose_name=_('is active'), default=True)
    date_joined = models.DateTimeField(verbose_name=_('date joined'), default=timezone.now)
    auth_provider = models.CharField(
        max_length=255, blank=False,null=False,
        default=AUTH_PROVIDERS.get(settings.EMAIL_AUTH_PROVIDER)
    )


    objects = CustomUserManager()

    def delete(self, using=None, keep_parents=False):
        super().delete()
