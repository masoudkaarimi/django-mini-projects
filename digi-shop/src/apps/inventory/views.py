from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from apps.inventory.models import ProductVariant


def variant_json(request, variant_id):
    """API endpoint to get product variant details for cart"""
    variant = get_object_or_404(ProductVariant, id=variant_id, is_active=True)
    product = variant.product

    # Get pricing info
    price = variant.pricing.current_price if hasattr(variant, 'pricing') else 0

    # Get featured image
    image_url = None
    featured_image = product.get_featured_image()
    if featured_image:
        image_url = featured_image.file.url

    return JsonResponse({
        'variant_id': variant.id,
        'product_id': product.id,
        'name': product.name,
        'variant_name': variant.name,
        'price': price,
        'image': image_url,
        'url': product.get_absolute_url(),
    })
