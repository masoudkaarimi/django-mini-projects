import logging
from datetime import timezone

from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in

from PIL import Image

from apps.account.models import Profile, Address, Wishlist

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def update_last_login_info(sender, request, user, **kwargs):
    try:
        user.last_login_ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or request.META.get('REMOTE_ADDR')
        user.last_login_at = timezone.now()
        user.save(update_fields=['last_login_ip', 'last_login_at'])
    except Exception as e:
        logger.error("Error updating last login info: %s", e)


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        logger.info("Profile created for user: %s", instance)


@receiver(post_save, sender=get_user_model())
def create_user_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def resize_profile_avatar(sender, instance, **kwargs):
    if instance.avatar:
        try:
            img = Image.open(instance.avatar.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300, 300))
                img.save(instance.avatar.path)
        except Exception as e:
            logger.error("Error resizing avatar image: %s", e)


@receiver(post_save, sender=Address)
def set_default_address(sender, instance, created, **kwargs):
    if instance.is_default:
        Address.objects.filter(user=instance.user, is_default=True).exclude(pk=instance.pk).update(is_default=False)
