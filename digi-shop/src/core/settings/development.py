from core.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", True)

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(",")

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_VERSION = "1.0.0"
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media files (user-uploaded files)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Django Vite Plugin
# DJANGO_VITE_PLUGIN["DEV_MODE"] = DEBUG
# DJANGO_VITE_PLUGIN["BUILD_URL_PREFIX"] = STATIC_URL
