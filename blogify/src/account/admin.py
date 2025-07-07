from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from account.forms import UserCreationAdminForm, UserChangeAdminForm
from account.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"
    readonly_fields = ("posts_count",)


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    model = get_user_model()
    inlines = [ProfileInline]
    add_form = UserCreationAdminForm
    form = UserChangeAdminForm
    list_display = ("id", "username", "email", "is_staff", "is_superuser", "is_active", "date_joined", "last_login")
    list_select_related = ('user_profile',)
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    readonly_fields = ("date_joined", "last_login", "last_login_ip")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal Information"), {"fields": ("first_name", "last_name", "email", "phone")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Security"), {"fields": ("date_joined", "last_login", "last_login_ip")}),
    )
    add_fieldsets = (
        (None, {"fields": ("username", "first_name", "last_name", "email", "phone", "password1", "password2", "groups", "is_staff", "is_superuser", "is_active")}),
    )
    search_fields = ("id", "username", "first_name", "last_name", "email", "phone")
    ordering = ("id",)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
