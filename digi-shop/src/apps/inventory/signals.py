from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete

from apps.inventory.models import ProductVariant, ProductMedia


@receiver(post_save, sender=ProductVariant)
def ensure_default_variant(sender, instance, created, **kwargs):
    """
    Ensure each product has a default variant by:
    1. Setting the first created variant as default if no default variant exists
    2. Maintaining only one default variant per product
    """
    product = instance.product

    # If this is the only variant for this product, make it default
    if product.variants.count() == 1:
        if not instance.is_default:
            instance.is_default = True
            # Use update to avoid recursive signal calls
            ProductVariant.objects.filter(pk=instance.pk).update(is_default=True)

    # If there's no default variant, make this one default
    elif not product.variants.filter(is_default=True).exists():
        instance.is_default = True
        # Use update to avoid recursive signal calls
        ProductVariant.objects.filter(pk=instance.pk).update(is_default=True)


@receiver(pre_save, sender=ProductVariant)
def maintain_single_default_variant(sender, instance, **kwargs):
    """Ensure only one variant can be default per product."""
    if instance.is_default:
        # This will set all other variants as not default
        ProductVariant.objects.filter(
            product=instance.product,
            is_default=True
        ).exclude(pk=instance.pk).update(is_default=False)


@receiver(post_delete, sender=ProductVariant)
def reassign_default_after_delete(sender, instance, **kwargs):
    """If the default variant is deleted, assign another variant as default."""
    if instance.is_default:
        # Find another variant to make default
        product = instance.product
        remaining_variant = product.variants.first()
        if remaining_variant:
            remaining_variant.is_default = True
            # Use update to avoid recursive signal calls
            ProductVariant.objects.filter(pk=remaining_variant.pk).update(is_default=True)


@receiver(post_save, sender=ProductMedia)
def ensure_featured_image(sender, instance, created, **kwargs):
    """
    Ensure each product has a featured image by:
    1. Setting the first uploaded image as featured if no featured image exists
    2. Maintaining only one featured image per product
    """
    if instance.type != ProductMedia.ProductMediaTypeChoices.IMAGE:
        return

    product = instance.product

    # If this is the only image for this product, make it featured
    if product.media.filter(type=ProductMedia.ProductMediaTypeChoices.IMAGE).count() == 1:
        if not instance.is_featured:
            instance.is_featured = True
            instance.save(update_fields=['is_featured'])

    # If there's no featured image, make this one featured
    elif not product.media.filter(
            is_featured=True,
            type=ProductMedia.ProductMediaTypeChoices.IMAGE
    ).exists():
        instance.is_featured = True
        instance.save(update_fields=['is_featured'])


@receiver(pre_save, sender=ProductMedia)
def maintain_single_featured_image(sender, instance, **kwargs):
    """Ensure only one image can be featured per product."""
    if instance.is_featured and instance.type == ProductMedia.ProductMediaTypeChoices.IMAGE:
        # This will set all other images as not featured
        ProductMedia.objects.filter(
            product=instance.product,
            type=ProductMedia.ProductMediaTypeChoices.IMAGE,
            is_featured=True
        ).exclude(pk=instance.pk).update(is_featured=False)
