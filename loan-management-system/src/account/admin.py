from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    """
    Custom User Admin
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("id", "username", "email", "is_staff", "is_superuser", "is_active", "date_joined", "last_login")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    readonly_fields = ("date_joined", "last_login", "last_ip")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal Information"), {"fields": ("first_name", "last_name", "email", "phone")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Security"), {"fields": ("date_joined", "last_login", "last_ip")}),
    )
    add_fieldsets = ((None, {"fields": ("first_name", "last_name", "username", "email", "phone", "password1", "password2", "groups", "is_staff", "is_active")}),)
    search_fields = ("id", "username", "email", "phone", "first_name", "last_name")
    ordering = ("id",)


admin.site.register(User, CustomUserAdmin)
