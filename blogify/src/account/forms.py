from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _

from phonenumber_field.formfields import PhoneNumberField


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=150,
        strip=True,
        required=True,
        # help_text=_(""),
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "autocomplete": "off",
                "class": "form-control",
                "name": "first_name",
                "id": "first_name",
                "placeholder": _("First Name"),
                "inputmode": "text",
            }
        )
    )

    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=150,
        strip=True,
        required=True,
        # help_text=_(""),
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "last_name",
                "id": "last_name",
                "placeholder": _("Last Name"),
                "inputmode": "text",
            }
        )
    )

    username = forms.CharField(
        label=_("Username"),
        max_length=150,
        strip=True,
        required=True,
        # help_text=_(""),
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "username",
                "id": "username",
                "placeholder": _("Username"),
                "inputmode": "text",
            }
        )
    )

    email = forms.EmailField(
        label=_("Email"),
        required=True,
        # help_text=_(""),
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "email",
                "id": "email",
                "pattern": "[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+",
                "placeholder": _("Email"),
                "inputmode": "email",
            }
        )
    )

    phone = PhoneNumberField(
        label=_("Phone Number"),
        strip=True,
        required=True,
        # help_text=_(""),
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "phone",
                "id": "phone",
                "placeholder": _("+1xxxxxxxxxx"),
                "inputmode": "tel",
            }
        )
    )

    password1 = forms.CharField(
        label=_("Password"),
        max_length=128,
        min_length=8,
        strip=False,
        required=True,
        # help_text=password_validators_help_text_html(),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "password1",
                "id": "password1",
                # "pattern": "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
                "placeholder": _("Password"),
                "inputmode": "text",
            }
        )
    )

    password2 = forms.CharField(
        label=_("Confirm Password"),
        max_length=128,
        min_length=8,
        strip=False,
        required=True,
        # help_text=_("Enter the same password as before, for verification."),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "password2",
                "id": "password2",
                # "pattern": "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
                "placeholder": _("Confirm Password"),
                "inputmode": "text",
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username", "email", "phone", "password1", "password2")


class LoginForm(forms.Form):
    identity = forms.CharField(
        label=_("Identity"),
        max_length=150,
        strip=True,
        required=True,
        # help_text=_(""),
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "Identity",
                "id": "Identity",
                "placeholder": _("Username / Email / Phone Number"),
                "inputmode": "text",
            }
        )
    )

    password = forms.CharField(
        label=_("Password"),
        max_length=128,
        min_length=8,
        strip=False,
        required=True,
        # help_text=password_validators_help_text_html(),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "password",
                "id": "password",
                # "pattern": "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
                "placeholder": _("Password"),
                "inputmode": "text",
            }
        )
    )


class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=150,
        strip=True,
        required=True,
        # help_text=_(""),
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "autocomplete": "off",
                # "class": "form-control",
                "name": "first_name",
                "id": "first_name",
                "placeholder": _("First Name"),
                "inputmode": "text",
            }
        )
    )

    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=150,
        strip=True,
        required=True,
        # help_text=_(""),
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                # "class": "form-control",
                "name": "last_name",
                "id": "last_name",
                "placeholder": _("Last Name"),
                "inputmode": "text",
            }
        )
    )

    username = forms.CharField(
        label=_("Username"),
        max_length=150,
        strip=True,
        required=True,
        # help_text=_(""),
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                # "class": "form-control",
                "name": "username",
                "id": "username",
                "placeholder": _("Username"),
                "inputmode": "text",
            }
        )
    )

    email = forms.EmailField(
        label=_("Email"),
        required=True,
        # help_text=_(""),
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "off",
                # "class": "form-control",
                "name": "email",
                "id": "email",
                "pattern": "[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+",
                "placeholder": _("Email"),
                "inputmode": "email",
            }
        )
    )

    phone = PhoneNumberField(
        label=_("Phone Number"),
        strip=True,
        required=True,
        # help_text=_(""),
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                # "class": "form-control",
                "name": "phone",
                "id": "phone",
                "placeholder": _("+1xxxxxxxxxx"),
                "inputmode": "tel",
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username", "email", "phone")


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        # help_text=_(""),
        widget=forms.EmailInput(
            attrs={
                "autofocus": True,
                "autocomplete": "off",
                "class": "form-control",
                "name": "email",
                "id": "email",
                "pattern": "[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+",
                "placeholder": _("Email"),
                "inputmode": "email"
            }
        ),
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        max_length=128,
        min_length=8,
        strip=False,
        required=True,
        # help_text=_(""),
        widget=forms.PasswordInput(
            attrs={
                "autofocus": True,
                "autocomplete": "off",
                "class": "form-control",
                "name": "new_password1",
                "id": "new_password1",
                "placeholder": _("New Password"),
                "inputmode": "text",
            }
        ),
    )

    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        max_length=128,
        min_length=8,
        strip=False,
        required=True,
        # help_text=_(""),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "new_password2",
                "id": "new_password2",
                "placeholder": _("Confirm New Password"),
                "inputmode": "text",
            }
        ),
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        max_length=128,
        min_length=8,
        strip=False,
        required=True,
        # help_text=_(""),
        widget=forms.PasswordInput(
            attrs={
                "autofocus": True,
                "autocomplete": "off",
                "class": "form-control",
                "name": "old_password",
                "id": "old_password",
                "placeholder": _("Old password"),
                "inputmode": "text",
            }
        ),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        max_length=128,
        min_length=8,
        strip=False,
        required=True,
        # help_text=_(""),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "new_password1",
                "id": "new_password1",
                "placeholder": _("New password"),
                "inputmode": "text",
            }
        ),
    )

    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        max_length=128,
        min_length=8,
        strip=False,
        required=True,
        # help_text=_(""),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "new_password2",
                "id": "new_password2",
                "placeholder": _("Confirm New Password"),
                "inputmode": "text",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = "__all__"


class UserCreationAdminForm(UserCreationForm):
    phone = PhoneNumberField(
        label=_("Phone Number"),
        strip=True,
        required=False,
        help_text=get_user_model()._meta.get_field("phone").help_text,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                # "class": "form-control",
                "name": "phone",
                "id": "phone",
                "placeholder": _("+1xxxxxxxxxx"),
                "inputmode": "tel",
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = "__all__"


class UserChangeAdminForm(UserChangeForm):
    phone = PhoneNumberField(
        label=_("Phone Number"),
        strip=True,
        required=False,
        help_text=get_user_model()._meta.get_field("phone").help_text,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                # "class": "form-control",
                "name": "phone",
                "id": "phone",
                "placeholder": _("+1xxxxxxxxxx"),
                "inputmode": "tel",
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = "__all__"
