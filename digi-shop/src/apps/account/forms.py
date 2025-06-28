from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm as UserChangeFormBase,
    PasswordChangeForm as PasswordChangeFormBase,
    PasswordResetForm as PasswordResetFormBase,
    SetPasswordForm as SetPasswordFormBase
)
from phonenumber_field.formfields import PhoneNumberField

from apps.account.models import Address, Profile

User = get_user_model()


class UserCreationAdminForm(UserCreationForm):
    phone_number = PhoneNumberField(
        label=_("Phone Number"),
        strip=True,
        required=False,
        help_text=User._meta.get_field("phone_number").help_text,
        widget=forms.TextInput(
            attrs={
                "name": "phone_number",
                "id": "phone_number",
                "placeholder": _("+1xxxxxxxxxx"),
                "inputmode": "tel",
            }
        )
    )

    class Meta:
        model = User
        fields = "__all__"


class UserChangeAdminForm(UserChangeFormBase):
    phone_number = PhoneNumberField(
        label=_("Phone Number"),
        strip=True,
        required=False,
        help_text=User._meta.get_field("phone_number").help_text,
        widget=forms.TextInput(
            attrs={
                "name": "phone_number",
                "id": "phone_number",
                "placeholder": _("+1xxxxxxxxxx"),
                "inputmode": "tel",
            }
        )
    )

    class Meta:
        model = User
        fields = "__all__"


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=150,
        strip=True,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-input",
                "name": "first_name",
                "id": "first_name",
                "placeholder": _("Enter your full name"),
                "inputmode": "text",
            }
        )
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=150,
        strip=True,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "last_name",
                "id": "last_name",
                "placeholder": _("Enter your full name"),
                "inputmode": "text",
            }
        )
    )
    username = forms.CharField(
        label=_("Username"),
        max_length=150,
        strip=True,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "username",
                "id": "username",
                "placeholder": _("Choose a username"),
                "inputmode": "text",
            }
        )
    )
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-input",
                "name": "email",
                "id": "email",
                "pattern": "[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+",
                "placeholder": _("your.email@example.com"),
                "inputmode": "email",
            }
        )
    )
    phone_number = PhoneNumberField(
        label=_("Phone Number"),
        strip=True,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "phone_number",
                "id": "phone_number",
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
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-input pe-10",
                "name": "password1",
                "id": "password1",
                "placeholder": _("Enter password"),
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
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-input pe-10",
                "name": "password2",
                "id": "password2",
                "placeholder": _("Confirm your password"),
                "inputmode": "text",
            }
        )
    )
    terms = forms.BooleanField(
        label=_("I accept the Terms and Conditions"),
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-checkbox",
                "name": "terms",
                "id": "terms",
            }
        )
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "phone_number", "password1", "password2", "terms")


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_("Username"),
        max_length=150,
        strip=True,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "username",
                "id": "username",
                "placeholder": _("Enter your username or email"),
                "inputmode": "text",
                "autofocus": True,
            }
        )
    )
    password = forms.CharField(
        label=_("Password"),
        max_length=128,
        min_length=8,
        strip=False,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-input",
                "name": "password",
                "id": "password",
                "placeholder": _("Enter your password"),
                "inputmode": "text",
            }
        )
    )


class UserChangeForm(UserChangeFormBase):
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=150,
        strip=True,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
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
        widget=forms.TextInput(
            attrs={
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

        widget=forms.TextInput(
            attrs={
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
        widget=forms.EmailInput(
            attrs={
                "name": "email",
                "id": "email",
                "pattern": "[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+",
                "placeholder": _("Email"),
                "inputmode": "email",
            }
        )
    )
    phone_number = PhoneNumberField(
        label=_("Phone Number"),
        strip=True,
        required=True,
        widget=forms.TextInput(
            attrs={
                "name": "phone_number",
                "id": "phone_number",
                "placeholder": _("+1xxxxxxxxxx"),
                "inputmode": "tel",
            }
        )
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "phone_number")


class PasswordResetForm(PasswordResetFormBase):
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "autofocus": True,
                "class": "form-input",
                "name": "email",
                "id": "email",
                "pattern": "[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+",
                "placeholder": _("your.email@example.com"),
                "inputmode": "email",
            }
        )
    )


class SetPasswordForm(SetPasswordFormBase):
    new_password1 = forms.CharField(
        label=_("New password"),
        max_length=128,
        min_length=8,
        strip=False,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "autofocus": True,
                "autocomplete": "off",
                "class": "form-input pe-10",
                "name": "new_password1",
                "id": "new_password1",
                "placeholder": _("New Password"),
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
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-input pe-10",
                "name": "new_password2",
                "id": "new_password2",
                "placeholder": _("Confirm New Password"),
                "inputmode": "text",
            }
        ),
    )


class PasswordChangeForm(PasswordChangeFormBase):
    old_password = forms.CharField(
        label=_("Old Password"),
        max_length=128,
        min_length=8,
        strip=False,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "autofocus": True,
                "autocomplete": "off",
                "class": "form-input",
                "name": "old_password",
                "id": "old_password",
                "placeholder": _("Old Password"),
                "inputmode": "text",
            }
        ),
    )
    new_password1 = forms.CharField(
        label=_("New Password"),
        max_length=128,
        min_length=8,
        strip=False,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-input",
                "name": "new_password1",
                "id": "new_password1",
                "placeholder": _("New Password"),
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
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-input",
                "name": "new_password2",
                "id": "new_password2",
                "placeholder": _("Confirm New Password"),
                "inputmode": "text",
            }
        ),
    )

    class Meta:
        model = User
        fields = "__all__"


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-input",
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
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "last_name",
                "id": "last_name",
                "placeholder": _("Last Name"),
                "inputmode": "text",
            }
        )
    )
    email = forms.EmailField(
        label=_("Email"),
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "form-input",
                "name": "email",
                "id": "email",
                "pattern": "[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+",
                "placeholder": _("your.email@example.com"),
                "inputmode": "email",
            }
        )
    )
    phone_number = PhoneNumberField(
        label=_("Phone Number"),
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "phone_number",
                "id": "phone_number",
                "placeholder": _("+1xxxxxxxxxx"),
                "inputmode": "tel",
            }
        ),
        help_text=Address._meta.get_field("phone_number").help_text,
    )
    avatar = forms.ImageField(
        label=_("Avatar"),
        required=False,
        help_text=_('The user\'s avatar. (Optional)<br />'
                    'The recommended size is <b>256x256px</b>.<br />'
                    'The supported formats are <b>{allowed_image_extensions}</b>.<br />'
                    'The maximum file size is <b>{max_size}MB</b>.').format(
            allowed_image_extensions=', '.join(settings.ALLOWED_IMAGE_EXTENSIONS),
            max_size=settings.MAX_IMAGE_SIZE / 1024
        ),
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-input",
                "name": "avatar",
                "id": "avatar",
            }
        ),
    )
    gender = forms.ChoiceField(
        choices=Profile.GenderChoices.choices,
        label=_("Gender"),
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-input",
                "name": "gender",
                "id": "gender",
            }
        ),
        help_text=_("Select the user's gender. (Optional)")
    )
    birthdate = forms.DateField(
        label=_("Birth Date"),
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-input",
                "name": "birthdate",
                "id": "birthdate",
                "type": "date",
            }
        ),
        help_text=_("The user's birthdate. (Optional)")
    )
    national_code = forms.CharField(
        label=_("National Code"),
        max_length=10,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "national_code",
                "id": "national_code",
                "placeholder": _("National Code"),
                "inputmode": "text",
            }
        ),
        help_text=_("The user's national code. (Optional)")
    )

    class Meta:
        model = Profile
        fields = ("avatar", "gender", "birthdate", "national_code")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['phone_number'].initial = getattr(self.instance.user, 'phone_number', '')

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = self.instance.user
        if user:
            user.first_name = self.cleaned_data.get('first_name', user.first_name)
            user.last_name = self.cleaned_data.get('last_name', user.last_name)
            user.email = self.cleaned_data.get('email', user.email)
            if 'phone_number' in self.cleaned_data:
                setattr(user, 'phone_number', self.cleaned_data['phone_number'])
            if commit:
                user.save()
        if commit:
            profile.save()
        return profile


# class ProfileForm(forms.ModelForm):
#     first_name = forms.CharField(
#         label=_("First Name"),
#         max_length=150,
#         required=False,  # Changed to False to allow partial updates
#         widget=forms.TextInput(
#             attrs={
#                 "autofocus": True,
#                 "class": "form-input",
#                 "name": "first_name",
#                 "id": "first_name",
#                 "placeholder": _("First Name"),
#                 "inputmode": "text",
#             }
#         )
#     )
#     last_name = forms.CharField(
#         label=_("Last Name"),
#         max_length=150,
#         required=False,
#         widget=forms.TextInput(
#             attrs={
#                 "class": "form-input",
#                 "name": "last_name",
#                 "id": "last_name",
#                 "placeholder": _("Last Name"),
#                 "inputmode": "text",
#             }
#         )
#     )
#     email = forms.EmailField(
#         label=_("Email"),
#         required=False,
#         widget=forms.EmailInput(
#             attrs={
#                 "class": "form-input",
#                 "name": "email",
#                 "id": "email",
#                 "pattern": "[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+",
#                 "placeholder": _("your.email@example.com"),
#                 "inputmode": "email",
#             }
#         )
#     )
#     phone_number = PhoneNumberField(
#         label=_("Phone Number"),
#         required=False,
#         widget=forms.TextInput(
#             attrs={
#                 "class": "form-input",
#                 "name": "phone_number",
#                 "id": "phone_number",
#                 "placeholder": _("+1xxxxxxxxxx"),
#                 "inputmode": "tel",
#             }
#         ),
#         help_text=Address._meta.get_field("phone_number").help_text,
#     )
#
#     class Meta:
#         model = User
#         fields = ("first_name", "last_name", "email", "phone_number")
#
#     def __init__(self, *args, **kwargs):
#         self.partial = kwargs.pop('partial', False) if 'partial' in kwargs else False
#         super().__init__(*args, **kwargs)
#
#     def save(self, commit=True):
#         if self.partial:
#             instance = self.instance
#             for field_name, value in self.cleaned_data.items():
#                 if value != '' and value is not None:
#                     setattr(instance, field_name, value)
#             if commit:
#                 instance.save()
#             return instance
#         return super().save(commit)


class AddressForm(forms.ModelForm):
    title = forms.CharField(
        label=_("Address Title"),
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "title",
                "id": "title",
                "placeholder": _("Home, Office, ..."),
                "inputmode": "text",
            }
        ),
        help_text=Address._meta.get_field("title").help_text,
    )
    full_name = forms.CharField(
        label=_("Full Name"),
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "full_name",
                "id": "full_name",
                "placeholder": _("Recipient's full name"),
                "inputmode": "text",
            }
        ),
        help_text=Address._meta.get_field("full_name").help_text,
    )
    phone_number = PhoneNumberField(
        label=_("Phone Number"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "phone_number",
                "id": "phone_number",
                "placeholder": _("+1xxxxxxxxxx"),
                "inputmode": "tel",
            }
        ),
        help_text=Address._meta.get_field("phone_number").help_text,
    )
    country = forms.ChoiceField(
        label=_("Country/Region"),
        required=True,
        choices=Address._meta.get_field("country").choices,
        widget=forms.Select(
            attrs={
                "class": "hidden",
                "name": "country",
                "id": "country",
                "data-hs-select": '''{
                    "hasSearch": true,
                    "searchPlaceholder": "Search...",
                    "searchClasses": "block w-full sm:text-sm border-gray-200 rounded-lg focus:border-blue-500 focus:ring-blue-500 before:absolute before:inset-0 before:z-1 py-1.5 sm:py-2 px-3",
                    "searchWrapperClasses": "bg-white p-2 -mx-1 sticky top-0",
                    "placeholder": "Select country...",
                    "toggleTag": "<button type=\\"button\\" aria-expanded=\\"false\\"><span class=\\"me-2\\" data-icon></span><span class=\\"text-gray-800\\" data-title></span></button>",
                    "toggleClasses": "hs-select-disabled:pointer-events-none hs-select-disabled:opacity-50 relative py-3 ps-4 pe-9 flex gap-x-2 text-nowrap w-full cursor-pointer bg-white border border-gray-200 rounded-lg text-start text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                    "dropdownClasses": "mt-2 max-h-72 pb-1 px-1 space-y-0.5 z-20 w-full bg-white border border-gray-200 rounded-lg overflow-hidden overflow-y-auto [&::-webkit-scrollbar]:w-2 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-track]:bg-gray-100 [&::-webkit-scrollbar-thumb]:bg-gray-300",
                    "optionClasses": "py-2 px-4 w-full text-sm text-gray-800 cursor-pointer hover:bg-gray-100 rounded-lg focus:outline-hidden focus:bg-gray-100",
                    "optionTemplate": "<div><div class=\\"flex items-center\\"><div class=\\"me-2\\" data-icon></div><div class=\\"text-gray-800\\" data-title></div></div></div>",
                    "extraMarkup": "<div class=\\"absolute top-1/2 end-3 -translate-y-1/2\\"><svg class=\\"shrink-0 size-3.5 text-gray-500\\" xmlns=\\"http://www.w3.org/2000/svg\\" width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"2\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\"><path d=\\"m7 15 5 5 5-5\\"/><path d=\\"m7 9 5-5 5 5\\"/></svg></div>"
                }'''
            }
        ),
        help_text=Address._meta.get_field("country").help_text,
    )
    city = forms.CharField(
        label=_("City"),
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "city",
                "id": "city",
                "placeholder": _("City"),
                "inputmode": "text",
            }
        ),
        help_text=Address._meta.get_field("city").help_text,
    )
    state = forms.CharField(
        label=_("State/Province"),
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "state",
                "id": "state",
                "placeholder": _("State/Province"),
                "inputmode": "text",
            }
        ),
        help_text=Address._meta.get_field("state").help_text,
    )
    zip_code = forms.CharField(
        label=_("Zip/Postal Code"),
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "zip_code",
                "id": "zip_code",
                "placeholder": _("Zip/Postal Code"),
                "inputmode": "text",
            }
        ),
        help_text=Address._meta.get_field("zip_code").help_text,
    )
    address_line_1 = forms.CharField(
        label=_("Address Line 1"),
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "address_line_1",
                "id": "address_line_1",
                "placeholder": _("Apartment, suite, etc."),
                "inputmode": "text",
            }
        ),
        help_text=Address._meta.get_field("address_line_1").help_text,
    )
    address_line_2 = forms.CharField(
        label=_("Address Line 2"),
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "address_line_2",
                "id": "address_line_2",
                "placeholder": _("Building, floor, etc. (optional)"),
                "inputmode": "text",
            }
        ),
        help_text=Address._meta.get_field("address_line_2").help_text,
    )
    is_default = forms.BooleanField(
        label=_("Set as default address"),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "peer sr-only",
                "name": "is_default",
                "id": "is_default",
            }
        ),
        help_text=Address._meta.get_field("is_default").help_text,
    )

    class Meta:
        model = Address
        fields = [
            "title",
            "full_name",
            "phone_number",
            "country",
            "city",
            "state",
            "zip_code",
            "address_line_1",
            "address_line_2",
            "is_default",
        ]
