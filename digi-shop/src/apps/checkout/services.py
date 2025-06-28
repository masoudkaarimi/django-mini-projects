import logging

from django.db.models import F
from django.utils import timezone
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from apps.inventory.models import ProductVariant
from apps.checkout.models import Cart, CartItem

logger = logging.getLogger(__name__)


class CartService:
    @staticmethod
    def get_or_create(user):
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    @staticmethod
    def add_item(user, product_variant_id, quantity=1):
        try:
            product_variant = ProductVariant.objects.select_related('product_variant').get(id=product_variant_id, is_active=True)

            # Check inventory
            if hasattr(product_variant, 'inventory'):
                if not product_variant.inventory.has_enough_quantity(quantity):
                    return False, _("Not enough inventories available")

            cart = CartService.get_or_create(user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product_variant=product_variant, defaults={'quantity': quantity})

            if not created:
                # Update existing item
                cart_item.quantity = F('quantity') + quantity
                cart_item.save(update_fields=['quantity', 'updated_at'])
                cart_item.refresh_from_db()

            # Reserve inventory
            cart_item.reserve(minutes=15)

            return cart_item, None

        except ProductVariant.DoesNotExist:
            return None, _("Product variant not found")
        except Exception as e:
            logger.error(f"Error adding to cart: {str(e)}")
            return None, _("An error occurred while adding to the cart")

    @staticmethod
    def update_item(user, product_variant_id, quantity):
        try:
            cart = CartService.get_or_create(user)
            cart_item = CartItem.objects.get(cart=cart, product_variant=product_variant_id)

            if quantity <= 0:
                cart_item.delete()
                return True, None

            # Check inventory
            if hasattr(cart_item.product_variant, 'inventory'):
                if not cart_item.product_variant.inventory.has_enough_quantity(quantity):
                    return False, _("Not enough inventories available")

            cart_item.quantity = quantity
            cart_item.save(update_fields=['quantity', 'updated_at'])

            # Reserve inventory
            cart_item.reserve(minutes=15)

            return True, None

        except CartItem.DoesNotExist:
            return False, _("Item not in cart")
        except Exception as e:
            logger.error(f"Error updating cart: {str(e)}")
            return False, _("An error occurred while updating the cart")

    @staticmethod
    def remove_item(user, product_variant_id):
        try:
            cart = CartService.get_or_create(user)
            CartItem.objects.filter(cart=cart, product_variant=product_variant_id).delete()
            return True, None
        except Exception as e:
            logger.error(f"Error removing from cart: {str(e)}")
            return False, _("An error occurred while removing from cart")

    @staticmethod
    def clear_items(user):
        try:
            cart = CartService.get_or_create(user)
            cart.clear()
            return True, None
        except Exception as e:
            logger.error(f"Error clearing cart: {str(e)}")
            return False, _("An error occurred while clearing cart")

    @staticmethod
    def sync_from_storage(user, storage_items):
        try:
            with transaction.atomic():
                cart = CartService.get_or_create(user)

                for item in storage_items:
                    product_variant_id = item.get('product_variant_id')
                    quantity = item.get('quantity', 1)

                    try:
                        product_variant = ProductVariant.objects.get(id=product_variant_id, is_active=True)
                        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_variant=product_variant, defaults={'quantity': quantity})

                        if not created:
                            # Keep higher quantity of local storage vs database
                            cart_item.quantity = max(cart_item.quantity, quantity)
                            cart_item.save(update_fields=['quantity', 'updated_at'])

                        # Reserve inventory
                        cart_item.reserve(minutes=15)

                    except ProductVariant.DoesNotExist:
                        continue

                return True, None

        except Exception as e:
            logger.error(f"Error syncing cart: {str(e)}")
            return False, _("An error occurred while syncing cart")

    @staticmethod
    def clear_expired_reservations():
        """Clear expired cart item reservations"""
        now = timezone.now()
        expired_items = CartItem.objects.filter(reserved_until__lt=now)
        count = expired_items.count()
        expired_items.update(reserved_until=None)
        return count

    @staticmethod
    def get_data(user):
        try:
            cart = CartService.get_or_create(user)
            items = []

            for item in cart.items.select_related('product_variant', 'product_variant__product', 'product_variant__pricing'):
                product_variant = item.product_variant
                product = product_variant.product
                price = product_variant.pricing.current_price if hasattr(product_variant, 'pricing') else 0
                stock = product_variant.inventory.available_quantity if hasattr(product_variant, 'inventory') else 0

                items.append({
                    'id': item.id,
                    'product_variant_id': product_variant.id,
                    'product_id': product.id,
                    'name': product.name,
                    'variant_name': product_variant.name,
                    'quantity': item.quantity,
                    'price': price,
                    'subtotal': item.subtotal,
                    'image': product.get_featured_image(),
                    'stock': stock,
                    'url': product.get_absolute_url(),
                    'reserved_until': item.reserved_until,

                    # 'id': item.id,
                    # 'quantity': item.quantity,
                    # 'stock': stock,
                    # 'price': price,
                    # 'subtotal': item.subtotal,
                    # 'reserved_until': item.reserved_until,
                    # 'product': {
                    #     "id": product.id,
                    #     'name': product.name,
                    #     'image': product.get_featured_image(),
                    #     'url': product.get_absolute_url(),
                    #     'variant': {
                    #         "id": product_variant.id,
                    #         "name": product_variant.name,
                    #     },
                    # },
                })

            return {
                'items': items,
                'total': cart.total,
                'item_count': cart.item_count,
            }

        except Exception as e:
            logger.error(f"Error getting cart data: {str(e)}")
            return {
                'items': [],
                'total': 0,
                'item_count': 0,
            }
