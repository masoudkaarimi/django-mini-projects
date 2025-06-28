from django.http import Http404
from django.urls import reverse
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, DetailView, ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from apps.shop.models import SliderBanner
from apps.inventory.models import Product, Brand, Category


class HomeView(TemplateView):
    template_name = 'shop/home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slider_banners = SliderBanner.objects.filter(is_active=True).order_by('order')[:2]
        categories = (Category.objects.annotate(product_count=Count('products')).order_by('-product_count')[:6])
        featured_products = Product.objects.filter(is_featured=True, is_active=True).order_by('-created_at')[:4]
        context.update({
            "slider_banners": slider_banners,
            "categories": categories,
            "featured_products": featured_products,
        })

        return context


# Todo: ContactView,AboutView,FAQView,TermsView

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
                {'title': _('Products'), 'url': reverse('shop:product_list')},
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
            context["stock_count"] = variant.inventory.quantity if hasattr(variant.inventory, "quantity") else 0
        else:
            context["price"] = None
            context["stock_count"] = 0

        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'shop/category/category_list.html'
    context_object_name = 'categories'
    paginate_by = 12
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
            {'title': _('Categories'), 'url': reverse('shop:category_list')},
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


class CheckoutView(TemplateView):
    template_name = 'shop/checkout/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        cart_items = []
        subtotal = 0

        for product_id, item in cart.items():
            try:
                product = Product.objects.get(id=product_id)
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
