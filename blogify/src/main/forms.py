from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        max_length=150,
        strip=True,
        required=True,
        # help_text=_(""),
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "name",
                "id": "name",
                "placeholder": _("Name"),
                "inputmode": "text",
            }
        )
    )

    subject = forms.CharField(
        label=_("Subject"),
        max_length=150,
        strip=True,
        required=True,
        # help_text=_(""),
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "subject",
                "id": "subject",
                "placeholder": _("Subject"),
                "inputmode": "text",
            }
        )
    )

    email = forms.EmailField(
        label=_("Email Address"),
        max_length=254,
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

    message = forms.CharField(
        label=_("Message"),
        strip=True,
        required=True,
        # help_text=_(""),
        widget=forms.Textarea(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "name": "message",
                "id": "message",
                "placeholder": _("Message"),
                "inputmode": "text",
            }
        )
    )
