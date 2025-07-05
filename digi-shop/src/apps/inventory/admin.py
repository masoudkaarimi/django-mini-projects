from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from mptt.admin import DraggableMPTTAdmin

from apps.inventory.models import (Brand, Category, Attribute, AttributeOption, ProductType, ProductTypeAttribute, Product, ProductAttribute, ProductVariant,
                                   ProductVariantAttribute, ProductMedia, Inventory, Pricing)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ['tree_actions', 'indented_title', 'is_active', 'order']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']


class AttributeOptionInline(admin.TabularInline):
    model = AttributeOption
    extra = 1


@admin.register(AttributeOption)
class AttributeOptionAdmin(admin.ModelAdmin):
    list_display = ['attribute', 'value', 'slug', 'order']
    list_filter = ['attribute']
    search_fields = ['value']
    prepopulated_fields = {'slug': ('value',)}
    ordering = ['attribute', 'order']


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'is_required', 'is_variant', 'is_filterable']
    list_filter = ['type', 'is_required', 'is_variant', 'is_filterable']
    search_fields = ['name', 'help_text']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [AttributeOptionInline]


class ProductTypeAttributeInline(admin.TabularInline):
    model = ProductTypeAttribute
    extra = 1


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProductTypeAttributeInline]


class ProductAttributeInline(admin.StackedInline):
    model = ProductAttribute
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['name', 'sku', 'is_default', 'is_active']


class ProductMediaInline(admin.TabularInline):
    model = ProductMedia
    extra = 1
    fields = ['type', 'file', 'alt_text', 'is_featured', 'order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'type', 'is_active', 'is_featured', 'view_count']
    list_filter = ['is_active', 'is_featured', 'is_digital', 'brand', 'type', 'created_at']
    search_fields = ['name', 'description', 'sku']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['categories']
    readonly_fields = ['created_at', 'updated_at', 'view_count']
    inlines = [ProductAttributeInline, ProductVariantInline, ProductMediaInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'short_description', 'sku')
        }),
        ('Relationships', {
            'fields': ('brand', 'type', 'categories')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'is_digital')
        }),
        ('Tracking', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


class ProductVariantAttributeInline(admin.TabularInline):
    model = ProductVariantAttribute
    extra = 1


class InventoryInline(admin.StackedInline):
    model = Inventory
    can_delete = False


class PricingInline(admin.TabularInline):
    model = Pricing
    extra = 1


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'sku', 'get_current_price', 'is_default', 'is_active', 'get_stock_status']
    list_filter = ['is_default', 'is_active', 'created_at']
    search_fields = ['name', 'sku', 'product__name']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ('product',)
    inlines = [ProductVariantAttributeInline, InventoryInline, PricingInline]

    @staticmethod
    def get_stock_status(obj):
        inventory = getattr(obj, 'inventory', None)

        if inventory:
            if inventory.available_quantity > 0:
                return format_html('<span style="color: green;">In Stock ({})</span>', inventory.available_quantity)
            else:
                return format_html('<span style="color: red;"> Out of Stock</span>')
        return format_html('<span style="color: orange;">Not Available</span>')

    def get_current_price(self, obj):
        pricing = obj.pricing

        return pricing.current_price if pricing else '-'

    get_stock_status.short_description = _('Stock Status')
    get_current_price.short_description = _('Current Price')


@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ['product', 'variant', 'type', 'is_featured', 'order']
    list_filter = ['type', 'is_featured', 'created_at']
    search_fields = ['product__name', 'alt_text']


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['variant', 'quantity', 'reserved_quantity', 'available_quantity', 'reorder_level', 'is_in_stock']
    list_filter = ['track_quantity', 'allow_backorders']
    search_fields = ['variant__name', 'variant__product__name']
    readonly_fields = ['available_quantity', 'is_in_stock']


# @admin.register(PricingTier)
# class PricingTierAdmin(admin.ModelAdmin):
#     list_display = ['name', 'is_default']
#     search_fields = ['name', 'description']
#

@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    list_display = ['variant', 'current_price', 'is_on_sale', 'currency']
    # list_display = ['variant', 'tier', 'current_price', 'is_on_sale', 'currency']
    # list_filter = ['tier', 'currency', 'created_at']
    list_filter = ['currency', 'created_at']
    search_fields = ['variant__name', 'variant__product__name']
    readonly_fields = ['current_price', 'is_on_sale']

    fieldsets = (
        ('Basic Information', {
            # 'fields': ('variant', 'tier', 'currency')
            'fields': ('variant', 'currency')
        }),
        ('Pricing', {
            'fields': ('cost_price', 'base_price', 'sale_price')
        }),
        ('Sale Period', {
            'fields': ('sale_start_date', 'sale_end_date'),
            'classes': ('collapse',)
        }),
        ('Calculated Fields', {
            'fields': ('current_price', 'is_on_sale'),
            'classes': ('collapse',)
        })
    )
