import math

from django.urls import reverse
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.utils.translation import gettext_lazy as _

from apps.inventory.mixins import ProductFilterMixin
from apps.inventory.models import Product, Brand, Category, ProductVariant


class ProductListView(ListView, ProductFilterMixin):
    model = Product
    template_name = 'shop/product/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    ordering = ['-created_at']

    filters = ('brand', 'category', 'price', 'color', 'size', 'sorting',)
    sorts = ('default', 'popular', 'newest', 'name', 'price_asc', 'price_desc',)

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        # Apply filters to the queryset
        return self.filter_products(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Important: Get the unfiltered queryset for filter options
        products_queryset = Product.objects.filter(is_active=True)

        # Get filter context - this handles pagination and filtering
        filter_context = self.get_filter_context(products_queryset)

        # Add filter context to the main context
        context.update(filter_context)

        # Additional context data - FIXED: using correct field name 'products' instead of 'product'
        top_categories = (Category.objects.filter(products__isnull=False)
                          .annotate(product_count=Count('products', distinct=True))
                          .order_by('-product_count')[:6])

        top_brands = (Brand.objects.filter(products__isnull=False)
                      .annotate(product_count=Count('products', distinct=True))
                      .order_by('-product_count')[:6])

        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Products'), 'url': None},
            ],
            "heading": {
                "title": _("All Products"),
                "subtitle": _("Discover our collection of high-quality products."),
            },
            "categories": top_categories,
            "brands": top_brands,
        })

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if hasattr(self.request, 'product_viewed_signal'):
            self.request.product_viewed_signal.send(sender=self.__class__, instance=obj, request=self.request)
        return obj

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Products'), 'url': reverse('inventory:product_list')},
                {'title': product.name, 'url': None},
            ],
            "images": product.media.all(),
            "specifications": product.attribute_values.select_related('attribute').all(),
            "brand": product.brand,
            "categories": Product.objects.values('categories__name', 'categories__slug').annotate(product_count=Count('id')).order_by('-product_count')[:6],
            "similar_products": Product.objects.filter(categories__in=product.categories.all()).exclude(id=product.id).distinct().order_by('?')[:6],
            'color_options': product.get_color_options(),
            'size_options': product.get_size_options(),
            'pricing': product.get_pricing(),
            'inventory': product.get_inventory(),
        })

        # Get pricing and inventory from default variant
        variant = product.get_default_variant()
        if variant:
            context["price"] = variant.pricing.current_price if hasattr(variant, 'pricing') else None
            try:
                context["stock_count"] = variant.inventory.quantity if variant.inventory else 0
            except ProductVariant.inventory.RelatedObjectDoesNotExist:
                context["stock_count"] = 0
        else:
            context["price"] = None
            context["stock_count"] = 0

        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'shop/category/category_list.html'
    context_object_name = 'categories'
    ordering = ['-created_at']

    def get_queryset(self):
        return Category.objects.filter(is_active=True, parent=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Categories'), 'url': None},
            ],
            "heading": {
                "title": _("All Categories"),
                "subtitle": _("Browse through our categories to find what you need."),
            },
        })
        return context


class CategoryProductListView(ListView, ProductFilterMixin):
    model = Product
    template_name = 'shop/category/category_detail.html'
    context_object_name = 'products'
    paginate_by = 20
    filters = ('brand', 'price', 'color', 'size', 'sorting',)
    sorts = ('default', 'popular', 'newest', 'name', 'price_asc', 'price_desc',)

    def get_queryset(self):
        category = self.get_category()
        queryset = Product.objects.filter(
            categories__in=category.get_descendants(include_self=True),
            is_active=True
        ).distinct()

        return self.filter_products(queryset)

    def get_category(self):
        path = self.kwargs.get('path', '').strip('/')
        slugs = path.split('/')
        category = get_object_or_404(Category, slug=slugs[0], parent=None, is_active=True)

        for slug in slugs[1:]:
            category = get_object_or_404(Category, slug=slug, parent=category, is_active=True)

        return category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_category()

        # Get the base products queryset for this category
        products_queryset = Product.objects.filter(
            categories__in=category.get_descendants(include_self=True),
            is_active=True
        ).distinct()

        # Get filter context with the category-specific queryset
        filter_context = self.get_filter_context(products_queryset)
        context.update(filter_context)

        # Additional context for the category
        context.update({
            "category": category,
            "breadcrumb": self.get_breadcrumb(category),
            "heading": {
                "title": category.name,
                "subtitle": _("Explore our collection of %(category)s products") % {"category": category.name},
            },
        })

        return context

    @staticmethod
    def get_breadcrumb(category):
        breadcrumb = [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Categories'), 'url': reverse('inventory:category_list')},
        ]

        ancestors = category.get_ancestors(include_self=True)
        for i, ancestor in enumerate(ancestors):
            breadcrumb.append({
                'title': ancestor.name,
                'url': None if i == len(ancestors) - 1 else ancestor.get_absolute_url()
            })

        return breadcrumb


class BrandListView(ListView):
    model = Brand
    template_name = 'shop/brand/brand_list.html'
    context_object_name = 'brands'
    paginate_by = 20
    ordering = ['-created_at']

    def get_queryset(self):
        return Brand.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Brands'), 'url': None},
            ],
            "heading": {
                "title": _("All Brands"),
                "subtitle": _("Browse through our extensive collection of brands."),
            },
        })

        return context


class BrandProductListView(ListView, ProductFilterMixin):
    model = Product
    template_name = 'shop/brand/brand_detail.html'
    context_object_name = 'products'
    paginate_by = 20
    filters = ('category', 'price', 'color', 'size', 'sorting',)
    sorts = ('default', 'popular', 'newest', 'name', 'price_asc', 'price_desc',)

    def get_queryset(self):
        brand = self.get_brand()
        queryset = Product.objects.filter(
            brand=brand,
            is_active=True
        ).distinct()

        # Apply filters to the queryset
        return self.filter_products(queryset)

    def get_brand(self):
        return get_object_or_404(Brand, slug=self.kwargs['slug'], is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = self.get_brand()

        # Get the brand-specific products queryset for filter options
        products_queryset = Product.objects.filter(
            brand=brand,
            is_active=True
        ).distinct()

        # Get filter context
        filter_context = self.get_filter_context(products_queryset)
        context.update(filter_context)

        # Additional context for the brand
        context.update({
            "brand": brand,
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Brands'), 'url': reverse('inventory:brand_list')},
                {'title': brand.name, 'url': None},
            ],
            "heading": {
                "title": brand.name,
                "subtitle": _("Explore our collection of %(brand)s products") % {"brand": brand.name},
            },
            "brand_details": {
                "description": brand.description,
                "logo": brand.get_logo_url(),
            }
        })

        return context
