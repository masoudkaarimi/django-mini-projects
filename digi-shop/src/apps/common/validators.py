from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _


def validate_file_size(value, max_size_kb=1024):
    if value.size > max_size_kb * 1024:
        raise ValidationError(_("The maximum file size is %(max_size_kb)sKB.", params={'max_size_kb': max_size_kb}))


def validate_file_extension(value, valid_extensions=None):
    return FileExtensionValidator(allowed_extensions=valid_extensions)(value)
