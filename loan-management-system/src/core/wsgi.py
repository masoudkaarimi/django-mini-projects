"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from .settings.base import DEBUG

if DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
    print("WSGI: Django loaded up in setting mode : \033[1;34mDevelopment\033[0m")
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')
    print("WSGI: Django loaded up in setting mode : \033[1;34mProduction\033[0m")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
