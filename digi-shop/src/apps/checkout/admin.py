from django.contrib import admin
from apps.checkout.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    fields = ('product_variant', 'quantity', 'reserved_until')
    raw_id_fields = ('product_variant',)
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item_count', 'total', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CartItemInline]

    def item_count(self, obj):
        return obj.item_count

    item_count.short_description = 'Items'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        promotion_prices.delay(obj.promo_reduction, obj.id)
        promotion_management.delay()
