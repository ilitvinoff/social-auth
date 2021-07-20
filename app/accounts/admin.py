from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import AdminUserChangeForm
from .models import UserAccount


@admin.register(UserAccount)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("email",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)
    list_display = ("email", "uuid", "is_staff", "is_active", "is_superuser", "date_joined")
    search_fields = ("email",)
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ("email",)

    form = AdminUserChangeForm
