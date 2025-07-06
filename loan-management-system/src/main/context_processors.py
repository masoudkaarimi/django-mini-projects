from django.conf import settings


def default(request):
    return {
        'static_version': settings.STATIC_VERSION
    }
