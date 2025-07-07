from django import forms
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.widgets import CKEditor5Widget

from blog.models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label=_("Content"),
        required=False,
        # help_text=_(""),
        widget=CKEditor5Widget(
            attrs={
                "autocomplete": "off",
                "name": "content",
                "placeholder": _("Write your comment here..."),
            }
        )
    )

    class Meta:
        model = Comment
        fields = ("post", "author", "parent", "content")
        widgets = {
            "post": forms.HiddenInput(),
            "author": forms.HiddenInput(),
            "parent": forms.HiddenInput(),
        }
