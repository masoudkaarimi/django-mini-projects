import secrets

from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.templatetags.static import static
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import TimeStampedModel
from apps.common.utils import generate_upload_path
from apps.account.validators import profile_avatar_validator


class User(AbstractUser, TimeStampedModel):
    class IdentityByEmailDoesNotExist(models.ObjectDoesNotExist):
        pass

    class IdentityByUsernameDoesNotExist(models.ObjectDoesNotExist):
        pass

    class IdentityByPhoneNumberDoesNotExist(models.ObjectDoesNotExist):
        pass

    date_joined = None
    last_login = None
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name=_("Email Address"),
        help_text=_("The email address that will be used to login. (Required)")
    )
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name=_('Phone Number'),
        help_text=_("The user's phone number. (Optional)")
    )
    # is_two_factor_enabled = models.BooleanField(
    #     default=False,
    #     verbose_name=_("Two-factor Authentication"),
    #     help_text=_("Whether two-factor authentication is enabled for this user.")
    # )
    # two_factor_secret = models.CharField(
    #     max_length=255,
    #     blank=True,
    #     null=True,
    #     verbose_name=_("2FA Secret"),
    #     help_text=_("Secret key for TOTP-based two-factor authentication.")
    # )
    # backup_codes = models.JSONField(
    #     default=list,
    #     blank=True,
    #     null=True,
    #     verbose_name=_("Backup Codes"),
    #     help_text=_("Backup codes for two-factor authentication recovery.")
    # )
    last_login_ip = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name=_("Last Login IP Address"),
        help_text=_("The IP address of the user's last login, if available. (Auto-generated)")
    )
    last_login_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Last Login Date"),
        help_text=_("The date and time of the user's last login, if available. (Auto-generated)")
    )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ['-id']

    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username

    def get_short_name(self):
        return self.first_name if self.first_name else self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # def generate_two_factor_secret(self):
    #     import pyotp
    #
    #     self.two_factor_secret = pyotp.random_base32()
    #     self.save(update_fields=['two_factor_secret'])
    #     return self.two_factor_secret
    #
    # def verify_two_factor_token(self, token):
    #     if not self.is_two_factor_enabled or not self.two_factor_secret:
    #         return False
    #
    #     import pyotp
    #
    #     totp = pyotp.TOTP(self.two_factor_secret)
    #     return totp.verify(token)
    #
    # def generate_backup_codes(self, count=10):
    #     import secrets
    #     import string
    #
    #     alphabet = string.ascii_uppercase + string.digits
    #     codes = [
    #         ''.join(secrets.choice(alphabet) for _ in range(8))
    #         for _ in range(count)
    #     ]
    #     self.backup_codes = codes
    #     self.save(update_fields=['backup_codes'])
    #     return codes

    def deactivate_account(self):
        # Anonymize personal data
        self.username = f"deleted_{self.pk}_{secrets.token_hex(6)}"
        self.email = f"{self.pk}_{secrets.token_hex(6)}@deleted.account"
        self.first_name = ""
        self.last_name = ""
        self.phone_number = None

        # Disable 2FA
        # self.is_two_factor_enabled = False
        # self.two_factor_secret = None
        # self.backup_codes = None

        # Clean up profile data if it exists
        try:
            if hasattr(self, 'profile'):
                profile = self.profile
                if profile.avatar:
                    profile.avatar.delete(save=False)  # Delete the file
                profile.avatar = None
                profile.save()
        except Exception:
            pass

        # Deactivate account
        self.is_active = False
        self.save()

        return True

    def delete_account(self, permanent=False):
        if permanent:
            # Permanently delete user and all related data
            self.delete()
            return True
        else:
            # Soft delete
            return self.deactivate_account()

    @classmethod
    def authenticate_email(cls, email, **kwargs):
        try:
            return cls.objects.get(email=email, **kwargs)
        except cls.DoesNotExist:
            raise cls.IdentityByEmailDoesNotExist(f'Identity by email: {email} does not exist.')
        except Exception as e:
            raise Exception(e)

    @classmethod
    def authenticate_username(cls, username, **kwargs):
        try:
            return cls.objects.get(username=username, **kwargs)
        except cls.DoesNotExist:
            raise cls.IdentityByUsernameDoesNotExist(f'Identity by username: {username} does not exist.')
        except Exception as e:
            raise Exception(e)

    @classmethod
    def authenticate_phone_number(cls, phone_number, **kwargs):
        try:
            return cls.objects.get(phone_number=phone_number, **kwargs)
        except cls.DoesNotExist:
            raise cls.IdentityByPhoneNumberDoesNotExist(f'Identity by phone number: {phone_number} does not exist.')
        except Exception as e:
            raise Exception(e)


class Profile(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'male', _('Male')
        FEMALE = 'female', _('Female')
        OTHER = 'other', _('Other')
        PREFER_NOT_TO_SAY = 'prefer_not_to_say', _('Prefer Not To Say')

    def avatar_path(instance, filename):
        return generate_upload_path(instance, filename, prefix='uploads/profiles', field_name=f"avatar_{instance.user.username}")

    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
        related_name="profile",
        blank=False,
        null=False,
        verbose_name=_("User"),
        help_text=_("The user that this profile belongs to. (Required)")
    )
    avatar = models.ImageField(
        upload_to=avatar_path,
        default=None,
        blank=True,
        null=True,
        validators=[profile_avatar_validator],
        verbose_name=_("Avatar"),
        help_text=_('The user\'s avatar. (Optional)<br />'
                    'The recommended size is <b>256x256px</b>.<br />'
                    'The supported formats are <b>{allowed_image_extensions}</b>.<br />'
                    'The maximum file size is <b>{max_size}MB</b>.').format(allowed_image_extensions=', '.join(settings.ALLOWED_IMAGE_EXTENSIONS),
                                                                            max_size=settings.MAX_IMAGE_SIZE / 1024)
    )
    gender = models.CharField(
        max_length=17,
        choices=GenderChoices.choices,
        default=GenderChoices.PREFER_NOT_TO_SAY,
        blank=True,
        null=True,
        verbose_name=_('Gender'),
        help_text=_("Select the user's gender. (Optional)")
    )
    birthdate = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Birth Date"),
        help_text=_("The user's birth date. (Optional)")
    )
    national_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name=_("National Code"),
        help_text=_("The user's national code. (Optional)")
    )

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
        ordering = ['-id']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return static('assets/images/placeholders/avatar.webp')


class Address(TimeStampedModel):
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="addresses",
        blank=False,
        null=False,
        verbose_name=_("User"),
        help_text=_("The user that this address belongs to. (Required)")
    )
    title = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name=_("Address Title"),
        help_text=_("A short title for the address, e.g., 'Home', 'Office'. (Optional)")
    )
    full_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name=_("Full Name"),
        help_text=_("The full name of the recipient at this address. (Required)")
    )
    phone_number = PhoneNumberField(
        blank=False,
        null=False,
        verbose_name=_("Phone Number"),
        help_text=_("The phone number of the recipient at this address. (Required)")
    )
    country = CountryField(
        blank=False,
        null=False,
        blank_label=_('(select country)'),
        verbose_name=_("Country/Region"),
        help_text=_("The country or region of the address. (Required)")
    )
    city = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name=_("City"),
        help_text=_("The city of the address. (Required)")
    )
    state = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name=_("State/Province"),
        help_text=_("The state or province of the address. (Required)")
    )
    zip_code = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        verbose_name=_("Zip/Postal Code"),
        help_text=_("The zip or postal code of the address. (Required)")
    )
    address_line_1 = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name=_("Address Line 1"),
        help_text=_("Additional address line, e.g., apartment or suite number. (Optional)")
    )
    address_line_2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Address Line 2"),
        help_text=_("Additional address line, e.g., building or floor number. (Optional)")
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name=_("Default Address"),
        help_text=_("Whether this is the default address for the user.")
    )

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")
        ordering = ['-id']

    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.country.name}"


class Wishlist(TimeStampedModel):
    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
        related_name='wishlist',
        blank=False,
        null=False,
        verbose_name=_("User"),
        help_text=_("The user who owns this wishlist."),
    )
    products = models.ManyToManyField(
        'inventory.Product',
        related_name='wishlists',
        verbose_name=_("Products"),
        help_text=_("Products added to this wishlist."),
        blank=True,
    )

    class Meta:
        verbose_name = _("Wishlist")
        verbose_name_plural = _("Wishlists")

    def __str__(self):
        return f"Wishlist of {self.user.username}"

    @property
    def item_count(self):
        return self.products.count()

# class Wallet and Transaction
