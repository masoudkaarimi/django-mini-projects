from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.account.forms import UserChangeAdminForm, UserCreationAdminForm
from apps.account.models import Profile, Address


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = _("Profile")
    verbose_name_plural = _("Profiles")
    fk_name = "user"


@admin.register(get_user_model())
class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeAdminForm
    add_form = UserCreationAdminForm
    inlines = [ProfileInline]
    ordering = ("id",)
    list_display = ("id", "username", "email", "is_staff", "is_superuser", "is_active",
                    "date_joined", "last_login")
    list_select_related = ('profile',)
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    readonly_fields = ("date_joined", "last_login", "last_login_ip")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal Information"), {"fields": ("first_name", "last_name", "email", "phone_number")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser",
                                       "groups", "user_permissions")}),
        (_("Security"), {"fields": ("date_joined", "last_login", "last_login_ip")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "first_name", "last_name", "email", "phone_number",
                       "password1", "password2", "groups", "is_staff",
                       "is_superuser", "is_active"),
        }),
    )

    search_fields = ("id", "username", "first_name", "last_name", "email", "phone_number")

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "address_line_1", "city", "country", "zip_code", "is_default")
    list_filter = ("country", "is_default")
    search_fields = ("user__username", "address_line_1", "city", "zip_code")
    ordering = ("-id",)

    # Todo: research this method
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
