import logging

from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in

from apps.account.models import Profile

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def update_last_login_ip(sender, request, user, **kwargs):
    try:
        user.last_login_ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or request.META.get('REMOTE_ADDR')
        user.save()
    except Exception as e:
        logger.error("Error updating last IP address: %s", e)


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        logger.info("Profile created for user: %s", instance)
