from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField

from account.validators import profile_avatar_validator, profile_cover_photo_validator
from main.utils import generate_upload_path


class User(AbstractUser):
    class IdentityByEmailDoesNotExist(models.ObjectDoesNotExist):
        pass

    class IdentityByUsernameDoesNotExist(models.ObjectDoesNotExist):
        pass

    class IdentityByPhoneDoesNotExist(models.ObjectDoesNotExist):
        pass

    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name=_("Email Address"),
        help_text=_("The email address that will be used to login. (Required)")
    )
    phone = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name=_('Phone Number'),
        help_text=_("The user's phone number. (Optional)")
    )
    last_login_ip = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name=_("Last Login IP Address"),
        help_text=_("The IP address of the user's last login, if available. (Auto-generated)")
    )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ['-id']

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("blog:author_posts_list", kwargs={"username": self.username})

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username

    def get_short_name(self):
        return self.first_name if self.first_name else self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

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
    def authenticate_phone(cls, phone, **kwargs):
        try:
            return cls.objects.get(phone=phone, **kwargs)
        except cls.DoesNotExist:
            raise cls.IdentityByPhoneDoesNotExist(f'Identity by phone: {phone} does not exist.')
        except Exception as e:
            raise Exception(e)


class Profile(models.Model):
    class GenderStatusChoices(models.TextChoices):
        MALE = 'male', _('Male')
        FEMALE = 'female', _('Female')
        OTHER = 'other', _('Other')
        PREFER_NOT_TO_SAY = 'prefer_not_to_say', _('Prefer Not To Say')

    def avatar_path(instance, filename):
        # return generate_upload_path(instance, filename, prefix='uploads/avatars')
        return generate_upload_path(instance, filename, prefix='uploads/profiles', filed_name=instance.user.username)

    def cover_path(instance, filename):
        # return generate_upload_path(instance, filename, prefix='uploads/covers')
        return generate_upload_path(instance, filename, prefix='uploads/profiles', filed_name=instance.user.username)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user_profile",
        blank=False,
        null=False,
        verbose_name=_("User"),
        help_text=_("The user that this profile belongs to. (Required)")
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Biography"),
        help_text=_("A short biography about the user. (Optional)")
    )
    avatar = models.ImageField(
        upload_to=avatar_path,
        default=static('assets/images/placeholders/avatar.webp'),
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
    cover_photo = models.ImageField(
        upload_to=cover_path,
        default=static('assets/images/placeholders/cover-photo.webp'),
        blank=True,
        null=True,
        validators=[profile_cover_photo_validator],
        verbose_name=_("Cover Photo"),
        help_text=_('The user\'s cover photo. (Optional)<br />'
                    'The recommended size is <b>1920x1080px</b>.<br />'
                    'The supported formats are <b>{allowed_image_extensions}</b>.<br />'
                    'The maximum file size is <b>{max_size}MB</b>.').format(allowed_image_extensions=', '.join(settings.ALLOWED_IMAGE_EXTENSIONS),
                                                                            max_size=settings.MAX_IMAGE_SIZE / 1024)
    )
    gender = models.CharField(
        max_length=17,
        choices=GenderStatusChoices.choices,
        default=GenderStatusChoices.PREFER_NOT_TO_SAY,
        blank=True,
        null=True,
        verbose_name=_('Gender'),
        help_text=_("Select the user's gender. (Optional)")
    )
    posts_count = models.IntegerField(
        default=0,
        editable=False,
        blank=False,
        null=False,
        verbose_name=_("Post Count"),
        help_text=_("The number of posts that the user has created. (Auto-generated)")
    )
    website_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Website URL"),
        help_text=_("The user's website URL. (Optional)")
    )
    facebook_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Facebook URL"),
        help_text=_("The user's Facebook profile URL. (Optional)")
    )
    twitter_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Twitter URL"),
        help_text=_("The user's Twitter profile URL. (Optional)")
    )
    instagram_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Instagram URL"),
        help_text=_("The user's Instagram profile URL. (Optional)")
    )
    linkedin_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("LinkedIn URL"),
        help_text=_("The user's LinkedIn profile URL. (Optional)")
    )

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
        ordering = ['-id']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return static('assets/images/placeholders/avatar.webp')

    def get_cover_photo(self):
        if self.cover_photo:
            return self.cover_photo.url
        return static('assets/images/placeholders/cover-photo.webp')
