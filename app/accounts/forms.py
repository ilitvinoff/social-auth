from django.contrib.auth import forms

from .models import UserAccount


class AdminUserChangeForm(forms.UserChangeForm):
    class Meta:
        model = UserAccount
        fields = "__all__"