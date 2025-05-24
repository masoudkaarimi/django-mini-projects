from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.inventory.models import (
    Brand,
    Category,
    Product,
    ProductType,
    ProductAttribute,
    ProductAttributeValue,
    ProductTypeAttribute,
    ProductInventory,
    ProductInventoryAttributeValue,
    Stock,
    Media
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'description')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active', 'level']
    list_filter = ['is_active', 'level']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'parent')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )


class ProductTypeAttributeInline(admin.TabularInline):
    model = ProductTypeAttribute
    extra = 1


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    inlines = [ProductTypeAttributeInline]


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ['product_attribute', 'value']
    list_filter = ['product_attribute']
    search_fields = ['value']


class ProductInventoryInline(admin.TabularInline):
    model = ProductInventory
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'category']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductInventoryInline]
    filter_horizontal = ['category']
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'description')
        }),
        (_('Category'), {
            'fields': ('category',)
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )


class ProductInventoryAttributeValueInline(admin.TabularInline):
    model = ProductInventoryAttributeValue
    extra = 1


class StockInline(admin.StackedInline):
    model = Stock


class MediaInline(admin.TabularInline):
    model = Media
    extra = 1


@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'sku', 'brand', 'is_default', 'is_active', 'retail_price']
    list_filter = ['is_default', 'is_active', 'brand', 'product_type']
    search_fields = ['sku', 'upc', 'product__name']
    inlines = [ProductInventoryAttributeValueInline, StockInline, MediaInline]
    fieldsets = (
        (_('Product Information'), {
            'fields': ('product', 'product_type', 'brand')
        }),
        (_('Inventory Details'), {
            'fields': ('sku', 'upc')
        }),
        (_('Pricing'), {
            'fields': ('retail_price', 'store_price', 'sale_price')
        }),
        (_('Physical Attributes'), {
            'fields': ('weight',)
        }),
        (_('Status'), {
            'fields': ('is_default', 'is_active')
        }),
    )


@admin.register(ProductInventoryAttributeValue)
class ProductInventoryAttributeValueAdmin(admin.ModelAdmin):
    list_display = ['product_inventory', 'attribute_value']
    list_filter = ['attribute_value__product_attribute']
    search_fields = ['product_inventory__product__name', 'attribute_value__value']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['product_inventory', 'units', 'units_sold', 'last_checked']
    list_filter = ['last_checked']
    search_fields = ['product_inventory__product__name']


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['product_inventory', 'alt_text', 'is_featured']
    list_filter = ['is_featured']
    search_fields = ['product_inventory__product__name', 'alt_text']
