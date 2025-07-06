import logging

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def update_last_ip_address(sender, request, user, **kwargs):
    """
    Updates the user's last IP address on login.
    """
    try:
        user.last_ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or request.META.get('REMOTE_ADDR')
        user.save()
    except Exception as e:
        logger.error("Error updating last IP address: %s", e)
