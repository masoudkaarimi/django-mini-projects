from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.password_validation import password_validators_help_text_html
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from account.models import User
from loan.models import Loan, Installment


class LoanAdminForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["user", "number", "name", "amount", "interest_rate", "installment_choice", "installment_count", "start_date"]

    def clean(self):
        cleaned_data = super().clean()
        installment_choice = cleaned_data.get("installment_choice")
        installment_count = cleaned_data.get("installment_count")

        if installment_choice == '0' and installment_count <= 0:
            raise forms.ValidationError("Invalid value for the number of installments.")
        return cleaned_data


class InstallmentAdminForm(forms.ModelForm):
    class Meta:
        model = Installment
        fields = ["loan", 'number', "due_date", "amount", "status", "description"]


class LoanCreateForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["name", "amount", "interest_rate", "installment_choice", "installment_count", "start_date"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "form-control",
                    "name": "name",
                    "id": "name",
                    "placeholder": _("Loan Name"),
                    "inputmode": "text",
                    "autofocus": True,
                }
            ),
            "amount": forms.NumberInput(
                attrs={
                    "autocomplete": "off",
                    "class": "form-control",
                    "name": "amount",
                    "id": "amount",
                    "placeholder": _("Loan Amount"),
                    "inputmode": "numeric",
                }
            ),
            "interest_rate": forms.NumberInput(
                attrs={
                    "autocomplete": "off",
                    "class": "form-control",
                    "name": "interest_rate",
                    "id": "interest_rate",
                    "placeholder": _("Interest Rate (%)"),
                    "inputmode": "numeric",
                }
            ),
            "installment_choice": forms.Select(
                attrs={
                    "autocomplete": "off",
                    "class": "form-control",
                    "name": "installment_choice",
                    "id": "installment_choice",
                    "placeholder": _("Installment Plan"),
                }
            ),
            "installment_count": forms.NumberInput(
                attrs={
                    "autocomplete": "off",
                    "class": "form-control",
                    "name": "installment_count",
                    "id": "installment_count",
                    "placeholder": _("Installment Count"),
                    "inputmode": "numeric",
                }
            ),
            # "start_date": forms.DateTimeInput(
            #     attrs={
            #         "autocomplete": "off",
            #         "class": "form-control",
            #         "name": "start_date",
            #         "id": "start_date",
            #         "placeholder": _("Start Date"),
            #     }
            # ),
        }

    def clean(self):
        cleaned_data = super().clean()
        installment_choice = cleaned_data.get("installment_choice")
        installment_count = cleaned_data.get("installment_count")

        if installment_choice == '0' and installment_count <= 0:
            raise forms.ValidationError("Invalid value for the number of installments.")
        return cleaned_data


class LoanUpdateForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["name", "amount", "interest_rate", "installment_choice", "installment_count", "start_date"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "autocomplete": "off",
                    "class": "form-control",
                    "name": "name",
                    "id": "name",
                    "placeholder": _("Loan Name"),
                    "inputmode": "text",
                    "autofocus": True,
                }
            ),
            "amount": forms.NumberInput(
                attrs={
                    "autocomplete": "off",
                    "class": "form-control",
                    "name": "amount",
                    "id": "amount",
                    "placeholder": _("Loan Amount"),
                    "inputmode": "numeric",
                }
            ),
            "interest_rate": forms.NumberInput(
                attrs={
                    "autocomplete": "off",
                    "class": "form-control",
                    "name": "interest_rate",
                    "id": "interest_rate",
                    "placeholder": _("Interest Rate (%)"),
                    "inputmode": "numeric",
                }
            ),
            "installment_choice": forms.Select(
                attrs={
                    "autocomplete": "off",
                    "class": "form-control",
                    "name": "installment_choice",
                    "id": "installment_choice",
                    "placeholder": _("Installment Plan"),
                }
            ),
            "installment_count": forms.NumberInput(
                attrs={
                    "autocomplete": "off",
                    "class": "form-control",
                    "name": "installment_count",
                    "id": "installment_count",
                    "placeholder": _("Installment Count"),
                    "inputmode": "numeric",
                }
            ),
            # "start_date": forms.DateTimeInput(
            #     attrs={
            #         "autocomplete": "off",
            #         "class": "form-control",
            #         "name": "start_date",
            #         "id": "start_date",
            #         "placeholder": _("Start Date"),
            #     }
            # ),
        }

    def clean(self):
        cleaned_data = super().clean()
        installment_choice = cleaned_data.get("installment_choice")
        installment_count = cleaned_data.get("installment_count")

        if installment_choice == '0' and installment_count <= 0:
            raise forms.ValidationError("Invalid value for the number of installments.")
        return cleaned_data


class UserCreateAdminForm(UserCreationForm):
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=150,
        required=True,
        strip=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "first_name",
                "id": "first_name",
                "placeholder": _("First Name"),
                "inputmode": "text",
                "autofocus": True,
            }
        )
    )

    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=150,
        required=True,
        strip=False,
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
        required=True,
        strip=False,
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
        label=_("Email Address"),
        required=True,
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
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "phone",
                "id": "phone",
                "placeholder": "+98XXXXXXXXXX",
                "inputmode": "numeric",
            }
        )
    )

    password1 = forms.CharField(
        label=_("Password"),
        min_length=8,
        max_length=128,
        required=True,
        strip=False,
        help_text=password_validators_help_text_html(),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "password1",
                "id": "password1",
                "pattern": "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
                "placeholder": _("Password"),
                "inputmode": "text",
            }
        )
    )

    password2 = forms.CharField(
        label=_("Confirm Password"),
        min_length=8,
        max_length=128,
        required=True,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "password2",
                "id": "password2",
                "pattern": "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
                "placeholder": _("Confirm Password"),
                "inputmode": "text",
            }
        )
    )

    groups = forms.ModelMultipleChoiceField(
        label=_("Groups"),
        required=False,
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "autocomplete": "off",
                "class": "form-select",
                "name": "groups",
                "id": "groups",
                "role": "switch",
                "placeholder": _("Groups"),
            }
        )
    )

    is_staff = forms.BooleanField(
        label=_("Administrator"),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "autocomplete": "off",
                "class": "form-check-input",
                "name": "is_staff",
                "id": "is_staff",
            }
        )
    )

    is_superuser = forms.BooleanField(
        label=_("Super Admin"),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "autocomplete": "off",
                "class": "form-check-input",
                "name": "is_superuser",
                "id": "is_superuser",
            }
        )
    )

    is_active = forms.BooleanField(
        label=_("Active"),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "autocomplete": "off",
                "class": "form-check-input",
                "name": "is_active",
                "id": "is_active",
            }
        )
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "phone", "password1", "password2", 'groups', 'is_staff', 'is_active', 'is_superuser']


class UserUpdateAdminForm(UserChangeForm):
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=150,
        required=True,
        strip=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "first_name",
                "id": "first_name",
                "placeholder": _("First Name"),
                "inputmode": "text",
                "autofocus": True,
            }
        )
    )

    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=150,
        required=True,
        strip=False,
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
        required=True,
        strip=False,
        disabled=True,
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
        label=_("Email Address"),
        required=True,
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
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "phone",
                "id": "phone",
                "placeholder": "+98XXXXXXXXXX",
                "inputmode": "numeric",
            }
        )
    )

    groups = forms.ModelMultipleChoiceField(
        label=_("Groups"),
        required=False,
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "autocomplete": "off",
                "class": "form-select",
                "name": "groups",
                "id": "groups",
                "role": "switch",
                "placeholder": _("Groups"),
            }
        )
    )

    is_staff = forms.BooleanField(
        label=_("Administrator"),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "autocomplete": "off",
                "class": "form-check-input",
                "name": "is_staff",
                "id": "is_staff",
            }
        )
    )

    is_superuser = forms.BooleanField(
        label=_("Super Admin"),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "autocomplete": "off",
                "class": "form-check-input",
                "name": "is_superuser",
                "id": "is_superuser",
            }
        )
    )

    is_active = forms.BooleanField(
        label=_("Active"),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "autocomplete": "off",
                "class": "form-check-input",
                "name": "is_active",
                "id": "is_active",
            }
        )
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "phone", "password", "groups", "is_staff", "is_active", "is_superuser"]
