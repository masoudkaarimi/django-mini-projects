from django.conf import settings

from main.validators import validate_file_extension, validate_file_size


def post_thumbnail_validator(value):
    validate_file_extension(value=value, valid_extensions=settings.ALLOWED_IMAGE_EXTENSIONS)
    validate_file_size(value=value, max_size_kb=settings.MAX_IMAGE_SIZE)


def category_thumbnail_validator(value):
    validate_file_extension(value=value, valid_extensions=settings.ALLOWED_IMAGE_EXTENSIONS)
    validate_file_size(value=value, max_size_kb=settings.MAX_IMAGE_SIZE)
