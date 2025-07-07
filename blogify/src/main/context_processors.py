from django.conf import settings


def default(request):
    return {
        'static_version': settings.STATIC_VERSION,
        'site_name': settings.SITE_NAME,
    }
