import json

from django.views import View
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.checkout.services import CartService
from apps.inventory.models import ProductVariant, Product


class CartView(TemplateView):
    template_name = 'shop/cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Cart'), 'url': None},
            ],
            "heading": {
                "title": _("Shopping Cart"),
                "subtitle": _("Review your items before proceeding to checkout."),
            },
        })

        return context


class AddToCartView(View):
    def post(self, request):
        product_variant_id = request.POST.get('product_variant_id')
        quantity = int(request.POST.get('quantity', 1))

        if request.user.is_authenticated:
            # For logged-in users, use the database
            cart_item, error = CartService.add_item(request.user, product_variant_id, quantity)

            if error:
                return JsonResponse({
                    'success': False,
                    'message': str(error)
                }, status=400)

            # Get updated cart data
            cart_data = CartService.get_data(request.user)

            return JsonResponse({
                'success': True,
                'message': _('Item added to cart'),
                'cart_data': cart_data
            })

        # For guest users
        try:
            product_variant = ProductVariant.objects.select_related('product', 'pricing', 'inventory').get(id=product_variant_id, is_active=True)

            # Check inventory
            inventory_available = True
            inventory_message = ""

            if hasattr(product_variant, 'inventory'):
                inventory = product_variant.inventory
                if not inventory.has_enough_quantity(quantity):
                    inventory_available = False
                    inventory_message = _("Not enough inventory available")

            # Get product details
            product = product_variant.product
            price = product_variant.pricing.current_price if hasattr(product_variant, 'pricing') else 0

            return JsonResponse({
                'success': inventory_available,
                'message': inventory_message if not inventory_available else _('Item added to cart'),
                'product': {
                    'variant_id': product_variant.id,
                    'product_id': product.id,
                    'name': product.name,
                    'variant_name': product_variant.name,
                    'price': price,
                    'image': product.get_featured_image(),
                    'url': product.get_absolute_url(),
                }
            })

        except ProductVariant.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': _('Product variant not found')
            }, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({
                'success': False,
                'message': _('An error occurred')
            }, status=500)


class UpdateCartItemView(View):
    def post(self, request):
        product_variant_id = request.POST.get('product_variant_id')
        quantity = int(request.POST.get('quantity', 0))

        if request.user.is_authenticated:
            # For logged-in users, update in the database
            success, error = CartService.update_item(request.user, product_variant_id, quantity)

            if error:
                return JsonResponse({
                    'success': False,
                    'message': str(error)
                }, status=400)

            # Get updated cart data
            cart_data = CartService.get_data(request.user)

            return JsonResponse({
                'success': True,
                'message': _('Cart updated'),
                'cart_data': cart_data
            })

        # For guest users, the frontend will handle localStorage
        # Just check inventory if quantity > 0
        if quantity > 0:
            try:
                product_variant = ProductVariant.objects.select_related('inventory').get(id=product_variant_id, is_active=True)

                # Check inventory
                inventory_available = True
                inventory_message = ""

                if hasattr(product_variant, 'inventory'):
                    inventory = product_variant.inventory
                    if not inventory.has_enough_quantity(quantity):
                        inventory_available = False
                        inventory_message = _("Not enough inventory available")

                return JsonResponse({
                    'success': inventory_available,
                    'message': inventory_message if not inventory_available else _('Cart updated'),
                })

            except ProductVariant.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': _('Product variant not found')
                }, status=404)
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': _('An error occurred')
                }, status=500)

        return JsonResponse({
            'success': True,
            'message': _('Item removed from cart')
        })


class RemoveFromCartView(View):
    def post(self, request):
        product_variant_id = request.POST.get('product_variant_id')

        if request.user.is_authenticated:
            # For logged-in users, remove from database
            success, error = CartService.remove_item(request.user, product_variant_id)

            if error:
                return JsonResponse({
                    'success': False,
                    'message': str(error)
                }, status=400)

            # Get updated cart data
            cart_data = CartService.get_data(request.user)

            return JsonResponse({
                'success': True,
                'message': _('Item removed from cart'),
                'cart_data': cart_data
            })

        # For guest users
        return JsonResponse({
            'success': True,
            'message': _('Item removed from cart')
        })


class ClearCartView(View):
    def post(self, request):
        if request.user.is_authenticated:
            # For logged-in users, clear database cart
            success, error = CartService.clear_items(request.user)

            if error:
                return JsonResponse({
                    'success': False,
                    'message': str(error)
                }, status=400)

            return JsonResponse({
                'success': True,
                'message': _('Cart cleared'),
                'cart_data': {'items': [], 'total': 0, 'item_count': 0}
            })

        # For guest users, the frontend will handle localStorage
        return JsonResponse({
            'success': True,
            'message': _('Cart cleared')
        })


class SyncCartView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            items = data.get('items', [])

            success, error = CartService.sync_from_storage(request.user, items)

            if error:
                return JsonResponse({
                    'success': False,
                    'message': str(error)
                }, status=400)

            # Get updated cart data
            cart_data = CartService.get_data(request.user)

            return JsonResponse({
                'success': True,
                'message': _('Cart synchronized'),
                'cart_data': cart_data
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': _('Invalid data format')
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': _('An error occurred')
            }, status=500)


class CheckInventoryView(View):
    def get(self, request, product_variant_id):
        quantity = int(request.GET.get('quantity', 1))

        try:
            variant = ProductVariant.objects.select_related('inventory').get(id=product_variant_id, is_active=True)
            available = True
            available_quantity = 0

            if hasattr(variant, 'inventory'):
                inventory = variant.inventory
                available_quantity = inventory.available_quantity

                if inventory.track_quantity:
                    available = inventory.has_enough_quantity(quantity)

            return JsonResponse({
                'available': available,
                'available_quantity': available_quantity,
                'message': _('Out of stock') if not available else _('In stock')}
            )

        except ProductVariant.DoesNotExist:
            return JsonResponse({
                'available': False,
                'message': _('Product variant not found')
            }, status=404)


class CheckoutView(TemplateView):
    template_name = 'shop/checkout/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        cart_items = []
        subtotal = 0

        for product_id, item in cart.items():
            try:
                product = Product.objects.get(id=product_id, is_active=True)
                quantity = item.get('quantity', 1)
                price = float(product.price)
                item_total = price * quantity
                subtotal += item_total

                cart_items.append({
                    "name": product.name,
                    "price": f"{price:.2f}",
                    "quantity": quantity,
                    "image_url": product.image.url if product.image else "/static/assets/images/placeholder.svg",
                    "link": product.get_absolute_url(),
                })
            except Product.DoesNotExist:
                continue

        shipping_address = {
            "name": "John Doe",
            "address": "123 Main Street, Apt 4B",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "country": "United States"
        }

        payment = {
            "card_name": "John Doe",
            "card_type": "Visa",
            "card_last4": "4242"
        }

        tax = subtotal * 0.08
        shipping = 0.0
        total = subtotal + tax + shipping

        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Checkout'), 'url': None},
            ],
            "heading": {
                "title": _("Checkout"),
                "subtitle": _("Review your order details before completing your purchase."),
            },
            "cart_items": cart_items,
            "subtotal": f"{subtotal:.2f}",
            "tax": f"{tax:.2f}",
            "shipping": f"{shipping:.2f}",
            "total": f"{total:.2f}",
            "shipping_address": shipping_address,
            "payment": payment,
        })

        return context
