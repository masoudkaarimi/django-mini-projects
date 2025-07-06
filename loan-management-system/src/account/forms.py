from django import forms
from django.contrib.auth.password_validation import password_validators_help_texts, password_validators_help_text_html
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import User


class CustomPasswordResetForm(PasswordResetForm):
    """
    Custom form for resetting a password.
    """
    email = forms.EmailField(
        label=_("Email address"),
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "off",
                "autofocus": True,
                "class": "form-control",
                "name": "email",
                "id": "email",
                "placeholder": _("Your email here"),
                "inputmode": "email"
            }
        ),
    )


class CustomSetPasswordForm(SetPasswordForm):
    """
    Custom form for setting a new password.
    """
    new_password1 = forms.CharField(
        label=_("New password"),
        max_length=128,
        min_length=8,
        required=True,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "autofocus": True,
                "class": "form-control",
                "name": "new_password1",
                "id": "new_password1",
                "placeholder": _("New Password"),
            }
        ),
    )

    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        max_length=128,
        min_length=8,
        required=True,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "new_password2",
                "id": "new_password2",
                "placeholder": _("Confirm New Password"),
            }
        ),
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Custom form for changing a password.
    """
    old_password = forms.CharField(
        label=_("Old password"),
        max_length=128,
        min_length=8,
        required=True,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "autofocus": True,
                "class": "form-control",
                "name": "old_password",
                "id": "old_password",
                "placeholder": _("Old password"),
            }
        ),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        max_length=128,
        min_length=8,
        required=True,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "new_password1",
                "id": "new_password1",
                "placeholder": _("New password"),
            }
        ),
    )

    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        max_length=128,
        min_length=8,
        required=True,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "new_password2",
                "id": "new_password2",
                "placeholder": _("Confirm New Password"),
            }
        ),
    )

    class Meta:
        model = User
        fields = "__all__"


class StylesCustomUserChangeForm(UserChangeForm):
    """
    Custom form for changing user information.
    """
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "first_name",
                "id": "first_name",
                "placeholder": _("First Name"),
            }
        )
    )

    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "last_name",
                "id": "last_name",
                "placeholder": _("Last Name"),
            }
        )
    )

    email = forms.EmailField(
        label=_("Email"),
        disabled=True,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "email",
                "id": "email",
                "placeholder": _("Email"),
            }
        )
    )

    phone = PhoneNumberField(
        label=_("Phone Number"),
        disabled=True,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "phone",
                "id": "phone",
                "placeholder": _("Phone Number"),
            }
        )
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone"]


class RegisterForm(UserCreationForm):
    """
    Custom form for creating a new user.
    """
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "first_name",
                "id": "first_name",
                "placeholder": _("First Name"),
            }
        )
    )

    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "last_name",
                "id": "last_name",
                "placeholder": _("Last Name"),
            }
        )
    )

    username = forms.CharField(
        label=_("Username"),
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "username",
                "id": "username",
                "placeholder": _("Username"),
            }
        )
    )

    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "email",
                "id": "email",
                "pattern": "[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+",
                "placeholder": _("Email"),
            }
        )
    )

    phone = PhoneNumberField(
        label=_("Phone Number"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "phone",
                "id": "phone",
                "placeholder": "+98XXXXXXXXXX",
            }
        )
    )

    password1 = forms.CharField(
        label=_("Password"),
        max_length=128,
        min_length=8,
        required=True,
        strip=False,
        help_text=password_validators_help_text_html(),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "password1",
                "id": "password1",
                # "pattern": "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
                "placeholder": "Password",
            }
        )
    )

    password2 = forms.CharField(
        label=_("Confirm Password"),
        max_length=128,
        min_length=8,
        required=True,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "password2",
                "id": "password2",
                # "pattern": "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
                "placeholder": "Confirm Password",
            }
        )
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "phone", "password1", "password2"]


class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for creating a new user.
    """
    phone = PhoneNumberField(
        required=False,
        widget=PhoneNumberPrefixWidget(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "phone",
                "id": "phone",
                "placeholder": "+98XXXXXXXXXX",
                "style": "margin-right:10px",
            }
        ),
    )

    class Meta:
        model = User
        fields = "__all__"


class CustomUserChangeForm(UserChangeForm):
    """
    Custom form for changing user information.
    """
    phone = PhoneNumberField(
        required=False,
        widget=PhoneNumberPrefixWidget(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "phone",
                "id": "phone",
                "placeholder": "+98XXXXXXXXXX",
                "style": "margin-right:10px"
            }
        ),
    )

    class Meta:
        model = User
        fields = "__all__"
