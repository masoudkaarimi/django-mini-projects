from django.http import Http404
from django.urls import reverse
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from apps.inventory.models import Product, Brand, Category, ProductVariant


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    ordering = ['-created_at']

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = (Product.objects.values('categories__id', 'categories__name', 'categories__slug').annotate(product_count=Count('id'))).order_by('-product_count')[:6]
        brands = (Product.objects.values('brand__id', 'brand__name', 'brand__slug').annotate(product_count=Count('id'))).order_by('-product_count')[:6]
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Products'), 'url': None},
            ],
            "heading": {
                "title": _("All Products"),
                "subtitle": _("Discover our collection of high-quality products."),
            },
            "categories": categories,
            "brands": brands,
        })

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

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


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'shop/category/category_detail.html'
    context_object_name = 'category'
    paginate_by = 2

    def get_object(self):
        path = self.kwargs.get('path', '').strip('/')
        if not path:
            raise Http404("Category path is required.")

        slugs = path.split('/')
        category = get_object_or_404(Category, slug=slugs[0], parent=None, is_active=True)

        for slug in slugs[1:]:
            category = get_object_or_404(Category, slug=slug, parent=category, is_active=True)

        return category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        sort = self.request.GET.get('sort', 'default')
        products_queryset = Product.objects.filter(categories__in=category.get_descendants(include_self=True), is_active=True).distinct()

        if sort == 'newest':
            products_queryset = products_queryset.order_by('-created_at')
        # elif sort == 'popular':
        # products_queryset = products_queryset.order_by('-popularity')
        elif sort == 'price_asc':
            products_queryset = products_queryset.order_by('price')
        elif sort == 'price_desc':
            products_queryset = products_queryset.order_by('-price')
        elif sort == 'name_asc':
            products_queryset = products_queryset.order_by('name')
        else:
            products_queryset = products_queryset.order_by('-id')

        paginator = Paginator(products_queryset, self.paginate_by)
        page_number = self.request.GET.get('page')

        try:
            products_page = paginator.page(page_number)
        except PageNotAnInteger:
            products_page = paginator.page(1)
        except EmptyPage:
            products_page = paginator.page(paginator.num_pages)

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

        context.update({
            "breadcrumb": breadcrumb,
            "heading": {
                "title": category.name,
                "subtitle": _("Explore our collection of %(category)s products") % {"category": category.name},
            },
            "products": products_page,
            "page_obj": products_page,
            "is_paginated": products_page.has_other_pages(),
            "sort": sort,
        })

        return context


class BrandListView(ListView):
    model = Brand
    template_name = 'shop/brand/brand_list.html'
    context_object_name = 'brands'
    paginate_by = 12
    ordering = ['-created_at']

    def get_queryset(self):
        return Brand.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # brands = (Product.objects.values(
        #     'brand__id',
        #     'brand__name',
        #     'brand__logo',
        #     'brand__slug'
        # ).annotate(product_count=Count('id'))).order_by('-product_count')[:6]
        context.update({
            "breadcrumb": [
                {'title': _('Home'), 'url': reverse('shop:home')},
                {'title': _('Brands'), 'url': None},
            ],
            "heading": {
                "title": _("All Brands"),
                "subtitle": _("Browse through our extensive collection of brands."),
            },
            # "brands": brands,
        })

        return context


class BrandDetailView(DetailView):
    model = Brand
    template_name = 'shop/brand/brand_detail.html'
    context_object_name = 'brand'
    paginate_by = 2


def variant_json(request, variant_id):
    """API endpoint to get product variant details for cart"""
    variant = get_object_or_404(ProductVariant, id=variant_id, is_active=True)
    product = variant.product

    # Get pricing info
    price = variant.pricing.current_price if hasattr(variant, 'pricing') else 0

    return JsonResponse({
        'variant_id': variant.id,
        'product_id': product.id,
        'name': product.name,
        'variant_name': variant.name,
        'price': price,
        'image': product.get_featured_image(),
        'url': product.get_absolute_url(),
    })
