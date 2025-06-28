from django.conf import settings

from apps.common.validators import validate_file_extension, validate_file_size


def profile_avatar_validator(value):
    validate_file_size(value=value, max_size_kb=settings.MAX_IMAGE_SIZE)
    validate_file_extension(value=value, valid_extensions=settings.ALLOWED_IMAGE_EXTENSIONS)
