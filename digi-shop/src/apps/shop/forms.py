from django import forms
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField


class ContactForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-input",
                "name": "name",
                "id": "name",
                "placeholder": _("Your Name"),
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
    subject = forms.CharField(
        label=_("Subject"),
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "subject",
                "id": "subject",
                "placeholder": _("Subject of your message"),
                "inputmode": "text",
            }
        )
    )
    message = forms.CharField(
        label=_("Message"),
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-input",
                "name": "message",
                "id": "message",
                "placeholder": _("Your message here..."),
                "rows": 5,
            }
        ),
        help_text=_("Please provide details about your inquiry.")
    )
