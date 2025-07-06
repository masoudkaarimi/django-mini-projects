import os

from .base import *

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(',')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_VERSION = "1.0.0"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# TODO: Add ckeditor to this project.
# CKEditor
# CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
# CKEDITOR_UPLOAD_PATH = "uploads/"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST", "postgres"),  # Use the service name from docker-compose.yml
        'PORT': os.getenv("DB_PORT", "5432"),
    }
}

# TODO: Add Cache to this project.
# CACHES = {
#     'default': {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         'LOCATION': os.getenv("REDIS_HOST"),  # Use the REDIS_HOST environment variable
#     }
# }

# Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
