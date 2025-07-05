from django.urls import reverse
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.utils.translation import gettext_lazy as _

from apps.inventory.mixins import ProductFilterMixin
from apps.inventory.models import Product, Brand, Category, ProductVariant, Attribute


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

    def get_queryset(self):
        return Product.objects.filter(is_active=True).prefetch_related('categories', 'variants__attribute_values__value_option')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if hasattr(self.request, 'product_viewed_signal'):
            self.request.product_viewed_signal.send(sender=self.__class__, instance=obj, request=self.request)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        variant_context = self._get_variant_data(product)
        context.update(variant_context)

        self._add_default_variant_data(context, product)

        context['breadcrumb'] = [
            {'title': _('Home'), 'url': reverse('shop:home')},
            {'title': _('Shop'), 'url': reverse('inventory:product_list')},
            {'title': product.name, 'url': None}
        ]

        similar_products = (
            Product.objects
            .filter(categories__in=product.categories.all(), type=product.type, is_active=True)
            .exclude(id=product.id)
            .select_related('brand')
            .prefetch_related('categories')
            .distinct()[:8]
        )
        context['similar_products'] = similar_products

        return context

    @staticmethod
    def _get_variant_data(product):
        color_attr = Attribute.objects.filter(type=Attribute.AttributeTypeChoices.COLOR).first()
        size_attr = Attribute.objects.filter(type=Attribute.AttributeTypeChoices.SIZE).first()

        active_variants = (
            product.variants
            .filter(is_active=True)
            .select_related('pricing', 'inventory')
            .prefetch_related('attribute_values__attribute', 'attribute_values__value_option')
        )

        variants_data = []
        variant_matrix = {}
        unique_colors = {}
        unique_sizes = {}

        for variant in active_variants:
            attr_values = {
                av.attribute_id: av for av in variant.attribute_values.all()
            }

            color_value = attr_values.get(color_attr.id) if color_attr else None
            size_value = attr_values.get(size_attr.id) if size_attr else None

            if color_value and size_value and color_value.value_option and size_value.value_option:
                color_id = str(color_value.value_option.id)
                size_id = str(size_value.value_option.id)

                if color_id not in unique_colors:
                    unique_colors[color_id] = {
                        'id': color_value.value_option.id,
                        'value': color_value.value_option.value,
                        'hex_code': color_value.value_option.hex_code
                    }

                if size_id not in unique_sizes:
                    unique_sizes[size_id] = {
                        'id': size_value.value_option.id,
                        'value': size_value.value_option.value
                    }

                variant_matrix[f"{color_id}_{size_id}"] = variant.id

                variants_data.append({
                    'id': variant.id,
                    'name': variant.name,
                    'sku': variant.sku,
                    'is_default': variant.is_default,
                    'base_price': float(variant.pricing.base_price) if hasattr(variant, 'pricing') else 0,
                    'current_price': float(variant.pricing.current_price) if hasattr(variant, 'pricing') else 0,
                    'is_on_sale': variant.pricing.is_on_sale if hasattr(variant, 'pricing') else False,
                    'sale_price': float(variant.pricing.current_price) if hasattr(variant, 'pricing') else 0,
                    'in_stock': variant.inventory.is_in_stock if hasattr(variant, 'inventory') else False,
                    'quantity': variant.inventory.available_quantity if hasattr(variant, 'inventory') else 0
                })

        return {
            'color_options': list(unique_colors.values()),
            'size_options': list(unique_sizes.values()),
            'variants_data': variants_data,
            'variant_matrix': variant_matrix
        }

    @staticmethod
    def _add_default_variant_data(context, product):
        default_variant = product.get_default_variant()
        if default_variant:
            context['pricing'] = getattr(default_variant, 'pricing', None)
            context['inventory'] = getattr(default_variant, 'inventory', None)


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
