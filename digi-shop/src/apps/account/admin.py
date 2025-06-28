from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.account.forms import UserChangeAdminForm, UserCreationAdminForm
from apps.account.models import Profile, Address, Wishlist


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = _("Profile")
    verbose_name_plural = _("Profiles")
    fk_name = "user"


class WishlistInline(admin.StackedInline):
    model = Wishlist
    can_delete = False
    verbose_name = _("Wishlist")
    verbose_name_plural = _("Wishlists")
    fk_name = "user"
    filter_horizontal = ("products",)
    extra = 0


class AddressInline(admin.TabularInline):
    model = Address
    fk_name = "user"
    verbose_name = _("Address")
    verbose_name_plural = _("Addresses")
    extra = 1


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    form = UserChangeAdminForm
    add_form = UserCreationAdminForm
    inlines = [ProfileInline, WishlistInline, AddressInline]
    ordering = ("id",)
    list_display = ("id", "username", "email", "is_staff", "is_superuser", "is_active", "created_at", "updated_at", "last_login")
    list_select_related = ('profile',)
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    readonly_fields = ("created_at", "updated_at", "last_login_at", "last_login_ip")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal Information"), {"fields": ("first_name", "last_name", "email", "phone_number")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser",
                                       "groups", "user_permissions")}),
        (_("Security"), {"fields": ("created_at", "updated_at", "last_login_at", "last_login_ip")}),
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


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product_count", "created_at", "updated_at")
    search_fields = ("user__username", "user__email")
    ordering = ("-id",)
    filter_horizontal = ("products",)
    autocomplete_fields = ("user", "products")
    readonly_fields = ("created_at", "updated_at")

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = _("Number of Products")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user").prefetch_related("products")
