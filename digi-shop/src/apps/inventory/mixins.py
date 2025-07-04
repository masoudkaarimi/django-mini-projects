import math
import logging

from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F, Max, OuterRef, Subquery, Case, When, DecimalField, Exists, Min
from django.utils.translation import gettext as _

from apps.inventory.models import Brand, Pricing, ProductVariantAttribute, Category

logger = logging.getLogger(__name__)


class ProductFilterMixin:
    # Configuration - only these properties will be used
    filters = ()  # Define which filters to activate
    sorts = ()  # Define which sort options to activate

    # Define request property for type checking
    request = None  # This will be set by the view that uses this mixin

    # Default filter configuration
    default_filter_config = {
        'brand': False,
        'category': False,
        'price': False,
        'color': False,
        'size': False,
        'sorting': True,  # Enable sorting by default
    }

    # Define default sort options - this will be the single source of truth
    sort_options = [
        {'value': 'default', 'label': _('Default')},
        {'value': 'popular', 'label': _('The most popular')},
        {'value': 'newest', 'label': _('Newest')},
        {'value': 'name', 'label': _('Name: A to Z')},
        {'value': 'price_asc', 'label': _('Price: Low to High')},
        {'value': 'price_desc', 'label': _('Price: High to Low')},
    ]

    def get_active_filters(self):
        """Determine which filters should be active based on configuration and request parameters"""
        if not hasattr(self, 'request') or not self.request:
            return self.default_filter_config.copy()

        filter_config = {}
        has_filter_restriction = bool(self.filters)

        for filter_name in self.default_filter_config:
            # First check if the filter is allowed by configuration
            if has_filter_restriction and filter_name not in self.filters:
                filter_config[filter_name] = False
                continue

            # For filters in self.filters, set them to True by default
            if has_filter_restriction:
                initial_status = True
            else:
                initial_status = self.default_filter_config.get(filter_name, False)

            filter_config[filter_name] = initial_status

            # Check for auto-activation based on filter parameters
            filter_params_exist = False
            if filter_name == 'brand' and self.request.GET.getlist('brand'):
                filter_params_exist = True
            elif filter_name == 'category' and self.request.GET.getlist('category'):
                filter_params_exist = True
            elif filter_name == 'price' and (self.request.GET.get('price_min') or self.request.GET.get('price_max')):
                filter_params_exist = True
            elif filter_name == 'color' and self.request.GET.getlist('color'):
                filter_params_exist = True
            elif filter_name == 'size' and self.request.GET.getlist('size'):
                filter_params_exist = True

            # Only apply URL parameter override if it exists
            param_value = self.request.GET.get(f'show_{filter_name}')
            if param_value is not None:
                filter_config[filter_name] = param_value.lower() in ('true', 'yes', '1', 'on')
            elif filter_params_exist:
                filter_config[filter_name] = True

        return filter_config

    def filter_products(self, queryset):
        """Apply all active filters to the queryset"""
        if not hasattr(self, 'request') or not self.request:
            return queryset

        active_filters = self.get_active_filters()
        original_count = queryset.count()

        # Brand filter
        if active_filters.get('brand'):
            brand_ids = self.request.GET.getlist('brand')
            if brand_ids:
                try:
                    brand_ids = [int(bid) for bid in brand_ids if bid.isdigit()]
                    if brand_ids:
                        queryset = queryset.filter(brand_id__in=brand_ids)
                except Exception as e:
                    logger.error(f"Error applying brand filter: {e}")

        # Category filter
        if active_filters.get('category'):
            category_ids = self.request.GET.getlist('category')
            if category_ids:
                try:
                    category_ids = [int(cid) for cid in category_ids if cid.isdigit()]
                    if category_ids:
                        queryset = queryset.filter(categories__id__in=category_ids)
                except Exception as e:
                    logger.error(f"Error applying category filter: {e}")

        # Price filter
        if active_filters.get('price'):
            price_min = self.request.GET.get('price_min')
            price_max = self.request.GET.get('price_max')

            if (price_min and price_min.isdigit()) or (price_max and price_max.isdigit()):
                try:
                    price_subquery = Pricing.objects.filter(
                        variant__product=OuterRef('pk'),
                        variant__is_default=True
                    ).values('base_price')[:1]
                    queryset = queryset.annotate(price=Subquery(price_subquery))

                    if price_min and price_min.isdigit():
                        queryset = queryset.filter(price__gte=price_min)
                    if price_max and price_max.isdigit():
                        queryset = queryset.filter(price__lte=price_max)

                except Exception as e:
                    logger.error(f"Error applying price filter: {e}")

        # Color filter
        if active_filters.get('color'):
            colors = self.request.GET.getlist('color')
            if colors:
                try:
                    color_variants = ProductVariantAttribute.objects.filter(
                        variant__product=OuterRef('pk'),
                        attribute__type='color',
                        value_option__value__in=colors
                    )
                    queryset = queryset.filter(Exists(color_variants))
                except Exception as e:
                    logger.error(f"Error applying color filter: {e}")

        # Size filter
        if active_filters.get('size'):
            sizes = self.request.GET.getlist('size')
            if sizes:
                try:
                    size_variants = ProductVariantAttribute.objects.filter(
                        variant__product=OuterRef('pk'),
                        attribute__type='size',
                        value_option__value__in=sizes
                    )
                    queryset = queryset.filter(Exists(size_variants))
                except Exception as e:
                    logger.error(f"Error applying size filter: {e}")

        # Always apply sorting regardless of filter settings
        sort_param = self.request.GET.get('sort')
        if sort_param:
            queryset = self.apply_sorting(queryset)

        filtered_count = queryset.count()

        return queryset

    def apply_sorting(self, queryset):
        """Apply sorting based on request parameters"""
        if not hasattr(self, 'request') or not self.request:
            return queryset

        sort = self.request.GET.get('sort', 'default')

        # Validate sort parameter if restrictions exist
        if self.sorts:
            sort_mapping = {
                'created_at': 'newest',
                'name': 'name_asc',
                'price': 'price_asc',
                'popularity': 'popular'
            }
            normalized_sort = sort_mapping.get(sort, sort)

            if normalized_sort not in self.sorts and sort != 'default':
                sort = 'default'

        # Apply sort
        try:
            if sort == 'newest' or sort == 'created_at':
                return queryset.order_by('-created_at')
            elif sort == 'name' or sort == 'name_asc':
                return queryset.order_by('name')
            elif sort == 'price' or sort == 'price_asc':
                return self.get_price_annotated_queryset(queryset).order_by('price')
            elif sort == 'price_desc':
                return self.get_price_annotated_queryset(queryset).order_by('-price')
            elif sort == 'popular' or sort == 'popularity':
                return queryset.order_by('-view_count')
            else:
                return queryset.order_by('-id')
        except Exception as e:
            logger.error(f"Error applying sort '{sort}': {e}")
            return queryset.order_by('-id')  # Fallback to default sort

    def paginate_queryset(self, queryset, page_size=None):
        """Paginate the queryset"""
        if page_size is None:
            page_size = getattr(self, 'paginate_by', 20)

        paginator = Paginator(queryset, page_size)
        page_number = self.request.GET.get('page', 1)

        try:
            return paginator.page(page_number)
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return paginator.page(paginator.num_pages)

    def get_sort_options(self):
        """Return available sort options based on configuration with URLs that preserve other query parameters"""
        options = []

        # Filter options based on configuration
        base_options = self.sort_options if not self.sorts else [
            option for option in self.sort_options
            if option['value'] == 'default' or option['value'] in self.sorts
        ]

        # Add URL to each option that preserves existing query parameters
        for option in base_options:
            enriched_option = option.copy()

            # Generate URL with preserved query parameters
            if hasattr(self, 'request') and self.request:
                params = self.request.GET.copy()
                params['sort'] = option['value']

                # Reset page when changing sort
                if 'page' in params:
                    params.pop('page')

                enriched_option['url'] = f"?{params.urlencode()}"
            else:
                enriched_option['url'] = f"?sort={option['value']}"

            options.append(enriched_option)

        return options

    def get_filter_context(self, products_queryset):
        """Generate context data for templates with filter information"""
        # Apply filters to queryset
        filtered_queryset = self.filter_products(products_queryset)

        # Get pagination
        page_size = getattr(self, 'paginate_by', 20)
        products_page = self.paginate_queryset(filtered_queryset, page_size)

        # Get filter configurations
        active_filters = self.get_active_filters()

        # Base context - always include these
        context = {
            "products": products_page,
            "page_obj": products_page,
            "is_paginated": getattr(products_page, 'has_other_pages', lambda: False)(),
            "active_filters": active_filters,
        }

        # Only add filters that are explicitly configured in self.filters
        configured_filters = set(self.filters)

        # Sort options - only add if 'sorting' is in configured filters
        if 'sorting' in configured_filters:
            context["sort"] = self.request.GET.get('sort', 'default')
            context["sort_options"] = self.get_sort_options()

        # Brand filter
        if 'brand' in configured_filters:
            context["brands"] = self.get_available_brands(products_queryset)
            selected_brands = []
            for brand_id in self.request.GET.getlist('brand'):
                if brand_id.isdigit():
                    selected_brands.append(int(brand_id))
            context["selected_brands"] = selected_brands

        # Category filter
        if 'category' in configured_filters:
            context["categories"] = self.get_available_categories(products_queryset)
            selected_categories = []
            for category_id in self.request.GET.getlist('category'):
                if category_id.isdigit():
                    selected_categories.append(int(category_id))
            context["selected_categories"] = selected_categories

        # Color filter
        if 'color' in configured_filters:
            context["available_colors"] = self.get_available_colors(products_queryset)
            context["selected_colors"] = self.request.GET.getlist('color')

        # Size filter
        if 'size' in configured_filters:
            context["available_sizes"] = self.get_available_sizes(products_queryset)
            context["selected_sizes"] = self.request.GET.getlist('size')

        # Price filter
        if 'price' in configured_filters:
            min_price, max_price = self.get_price_range(products_queryset)
            context["min_price"] = min_price
            context["max_price"] = max_price

        # Handle tuple pagination results (for backwards compatibility)
        if isinstance(products_page, tuple) and len(products_page) == 4:
            paginator, page, object_list, is_paginated = products_page
            context["products"] = page
            context["page_obj"] = page

        return context

    # Helper methods for fetching filter data
    @staticmethod
    def get_available_brands(products_queryset):
        brand_ids = products_queryset.values_list('brand_id', flat=True).distinct()
        brands = Brand.objects.filter(id__in=brand_ids)

        for brand in brands:
            brand.product_count = products_queryset.filter(brand_id=brand.id).count()

        return brands

    @staticmethod
    def get_available_colors(products_queryset):
        product_ids = products_queryset.values_list('id', flat=True)

        # Get unique color values by using values_list with distinct=True
        # and ordering by value to ensure consistent presentation
        colors = ProductVariantAttribute.objects.filter(
            variant__product_id__in=product_ids,
            attribute__type='color'
        ).values_list(
            'value_option__value',
            'value_option__hex_code'
        ).distinct().order_by('value_option__value')

        # Convert to the expected format
        return [{'value': color[0], 'hex_code': color[1]} for color in colors]

    @staticmethod
    def get_available_sizes(products_queryset):
        product_ids = products_queryset.values_list('id', flat=True)

        # Get unique size values
        sizes = ProductVariantAttribute.objects.filter(
            variant__product_id__in=product_ids,
            attribute__type='size'
        ).values_list('value_option__value', flat=True).distinct().order_by('value_option__value')

        # Sort sizes in a logical order
        size_order = {'xxs': 0, 'xs': 1, 's': 2, 'm': 3, 'l': 4, 'xl': 5, 'xxl': 6, '3xl': 7, '4xl': 8}
        result = []

        for value in sizes:
            try:
                order = float(value.replace(',', '.'))
            except (ValueError, AttributeError):
                # Handle potential None values or non-numeric strings
                order = size_order.get(value.lower() if value else '', 99)

            result.append({'value': value, 'order': order})

        return sorted(result, key=lambda x: x['order'])

    @staticmethod
    def get_available_categories(products_queryset):
        category_ids = products_queryset.values_list('categories__id', flat=True).distinct()
        categories = Category.objects.filter(id__in=category_ids)

        for category in categories:
            category.product_count = products_queryset.filter(categories__id=category.id).count()
        return categories

    @staticmethod
    def get_price_range(products_queryset):
        now = timezone.now()
        product_ids = products_queryset.values_list('id', flat=True)

        price_data = Pricing.objects.filter(
            variant__product_id__in=product_ids
        ).annotate(
            effective_price=Case(
                When(
                    sale_price__isnull=False,
                    sale_start_date__lte=now,
                    sale_end_date__gte=now,
                    then=F('sale_price')
                ),
                default=F('base_price'),
                output_field=DecimalField()
            )
        ).aggregate(
            min_price=Min('effective_price'),
            max_price=Max('effective_price')
        )

        min_price = math.floor(price_data['min_price'] / 10) * 10 if price_data['min_price'] else 0
        max_price = math.ceil(price_data['max_price'] / 100) * 100 if price_data['max_price'] else 1000

        return min_price, max_price

    @staticmethod
    def get_price_annotated_queryset(queryset):
        now = timezone.now()
        price_query = Pricing.objects.filter(
            variant__product=OuterRef('pk'),
            variant__is_default=True
        ).annotate(
            effective_price=Case(
                When(
                    sale_price__isnull=False,
                    sale_start_date__lte=now,
                    sale_end_date__gte=now,
                    then=F('sale_price')
                ),
                default=F('base_price'),
                output_field=DecimalField()
            )
        ).values('effective_price')[:1]

        return queryset.annotate(price=Subquery(price_query))
