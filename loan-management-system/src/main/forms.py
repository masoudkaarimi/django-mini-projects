from django import forms
from django.core.validators import MaxLengthValidator
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(label=_('Your Name'), min_length=3, max_length=100, required=True, help_text=_('Your full name'), error_messages={
        'required': _('Please enter your name.'),
        'min_length': _('Your name is too short.'),
        'max_length': _('Your name is too long.'),
    })
    email = forms.EmailField(label=_('Your Email'), max_length=100, required=True, help_text=_('Your email address'), error_messages={
        'required': _('Please enter your email address.'),
        'invalid': _('Please enter a valid email address.'),
        'max_length': _('Your email address is too long.'),
    })
    subject = forms.CharField(label=_('Subject'), max_length=100, required=True, help_text=_('Subject of your message'), error_messages={
        'required': _('Please enter a subject.'),
        'max_length': _('Your subject is too long.'),
    })
    message = forms.CharField(label=_('Message'), widget=forms.Textarea, validators=[MaxLengthValidator(1000)], required=True, help_text=_('Your message'), error_messages={
        'required': _('Please enter a message.'),
        'max_length': _('Your message is too long.'),
    })
