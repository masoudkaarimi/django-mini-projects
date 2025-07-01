from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.templatetags.static import static
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey, TreeManyToManyField

from apps.common.models import TimeStampedModel
from apps.common.utils import generate_upload_path


class ProductManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(is_active=True)

    def featured(self):
        return self.get_queryset().filter(is_featured=True, is_active=True)

    def by_category(self, category):
        return self.get_queryset().filter(categories=category, is_active=True)

    def by_brand(self, brand):
        return self.get_queryset().filter(brand=brand, is_active=True)


class Brand(TimeStampedModel):
    def brand_path(instance, filename):
        return generate_upload_path(instance, filename, prefix='uploads/brands/logos', field_name=f"logo_{instance.name}")

    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Brand Name"),
        help_text=_("The name of the brand. Must be unique. (Required)")
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Brand Slug"),
        help_text=_("URL-friendly version of the brand name. Used in URLs. (Required)")
    )
    logo = models.ImageField(
        upload_to=brand_path,
        null=True,
        blank=True,
        verbose_name=_("Brand Logo"),
        help_text=_("The brand's logo image. (Optional)")
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Brand Description"),
        help_text=_("Detailed description of the brand. (Optional)")
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name=_("Brand Visibility"),
        help_text=_("Controls whether the brand is visible to customers. (Default: Visible)")
    )

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_logo_url(self):
        if self.logo:
            return self.logo.url
        return static('assets/images/placeholders/brand.webp')


class Category(MPTTModel, TimeStampedModel):
    def category_path(instance, filename):
        return generate_upload_path(instance, filename, prefix='uploads/categories/icons', field_name=f"icon_{instance.name}")

    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Category Name"),
        help_text=_("The name of the category. Must be unique. (Required)")
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Category Slug"),
        help_text=_("URL-friendly version of the category name. Used in URLs. (Required)")
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        unique=False,
        null=True,
        blank=True,
        verbose_name=_("Parent Category"),
        help_text=_("Parent category if this is a subcategory. (Optional)")
    )
    image = models.ImageField(
        upload_to=category_path,
        null=True,
        blank=True,
        verbose_name=_("Category image"),
        help_text=_("The category's image. (Optional)")
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Category Description"),
        help_text=_("Detailed description of the category. (Optional)")
    )
    order = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name=_("Order"),
        help_text=_("The order in which categories are displayed. Lower numbers appear first. (Default: 0)")
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name=_("Category Visibility"),
        help_text=_("Controls whether the category is visible to customers. (Default: Visible)")
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        path = '/'.join(ancestor.slug for ancestor in self.get_ancestors(include_self=True))
        return reverse('inventory:category_detail', kwargs={'path': path})

    def get_image_url(self):
        if self.image:
            return self.image.url
        return static('assets/images/placeholders/category.webp')

    def get_full_path(self):
        return '/'.join([ancestor.slug for ancestor in self.get_ancestors(include_self=True)])


class Attribute(TimeStampedModel):
    class AttributeTypeChoices(models.TextChoices):
        TEXT = 'text', _("Text")
        NUMBER = 'number', _("Number")
        SELECT = 'select', _("Select")
        BOOLEAN = 'boolean', _("Boolean")
        DATETIME = 'datetime', _("DateTime")
        COLOR = 'color', _("Color")
        SIZE = 'size', _("Size")

    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Attribute Name"),
        help_text=_("The name of the attribute. Must be unique. (Required)")
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Attribute Slug"),
        help_text=_("URL-friendly version of the attribute name. Used in URLs. (Required)")
    )
    type = models.CharField(
        max_length=20,
        choices=AttributeTypeChoices.choices,
        default=AttributeTypeChoices.TEXT,
        null=False,
        blank=False,
        verbose_name=_("Attribute Type"),
        help_text=_("The type of the attribute. Choose from: text, number, date, boolean, choice, multiselect, color, size. (Required)")
    )
    is_required = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        verbose_name=_("Is Required"),
        help_text=_("Indicates if this attribute is required for products. (Default: No)")
    )
    is_variant = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        verbose_name=_("Is Variant"),
        help_text=_("Indicates if this attribute is used for product variants. (Default: No)")
    )
    is_filterable = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        verbose_name=_("Is Filterable"),
        help_text=_("Indicates if this attribute can be used for filtering products in search results. (Default: No)")
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name=_("Attribute Visibility"),
        help_text=_("Controls whether the attribute is visible to customers. (Default: Visible)")
    )
    unit = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Unit of Measurement"),
        help_text=_("The unit of measurement for this attribute, if applicable. (Optional)")
    )
    help_text = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Help Text"),
        help_text=_("Additional information or instructions for this attribute. (Optional)")
    )
    order = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name=_("Order"),
        help_text=_("The order in which attributes are displayed. Lower numbers appear first. (Default: 0)")
    )

    class Meta:
        verbose_name = _("Product Attribute")
        verbose_name_plural = _("Product Attributes")
        ordering = ['name']

    def __str__(self):
        return self.name


class AttributeOption(TimeStampedModel):
    attribute = models.ForeignKey(
        Attribute,
        related_name="options",
        on_delete=models.CASCADE,
        verbose_name=_("Attribute"),
        help_text=_("The attribute this option belongs to. (Required)")
    )
    value = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name=_("Option Value"),
        help_text=_("The value of the option for the attribute. (Required)")
    )
    hex_code = models.CharField(
        max_length=7,
        null=True,
        blank=True,
        verbose_name=_("Hex Color Code"),
        help_text=_("Hexadecimal color code for the option, used for Color type attributes. (Optional)")
    )
    order = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name=_("Order"),
        help_text=_("The order in which options are displayed. Lower numbers appear first. (Default: 0)")
    )

    class Meta:
        verbose_name = _("Attribute Option")
        verbose_name_plural = _("Attribute Options")
        ordering = ['order']
        unique_together = ('attribute', 'value')

    def __str__(self):
        return f"{self.attribute.name} - {self.value}"


class ProductType(TimeStampedModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Product Type Name"),
        help_text=_("The name of the product type. Must be unique. (Required)")
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Product Type Slug"),
        help_text=_("URL-friendly version of the product type name. Used in URLs. (Required)")
    )
    attributes = models.ManyToManyField(
        "Attribute",
        through='ProductTypeAttribute',
        related_name='product_types',
        blank=True,
        verbose_name=_("Attributes"),
        help_text=_("Attributes associated with this product type. (Optional)")
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Product Type Description"),
        help_text=_("Detailed description of the product type. (Optional)")
    )

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductTypeAttribute(models.Model):
    product_type = models.ForeignKey(
        "ProductType",
        on_delete=models.CASCADE,
        # related_name="product_type_attributes",
        verbose_name=_("Product Type"),
        help_text=_("The product type this attribute belongs to. (Required)")
    )
    attribute = models.ForeignKey(
        "Attribute",
        on_delete=models.CASCADE,
        # related_name="product_type_attributes",
        verbose_name=_("Attribute"),
        help_text=_("The attribute associated with this product type. (Required)")
    )
    is_required = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        verbose_name=_("Is Required"),
        help_text=_("Indicates if this attribute is required for products of this type. (Default: No)")
    )
    order = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name=_("Order"),
        help_text=_("The order in which attributes are displayed for this product type. Lower numbers appear first. (Default: 0)")
    )

    class Meta:
        verbose_name = _("Product Type Attribute")
        verbose_name_plural = _("Product Type Attributes")
        unique_together = ['product_type', 'attribute']
        ordering = ['order']


class Product(TimeStampedModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Product Name"),
        help_text=_("The name of the product. Must be unique. (Required)")
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Product Slug"),
        help_text=_("URL-friendly version of the product name. Used in URLs. (Required)")
    )
    short_description = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name=_("Short Description"),
        help_text=_("A brief description of the product. (Optional)")
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Product Description"),
        help_text=_("Detailed description of the product. (Optional)")
    )
    brand = models.ForeignKey(
        "Brand",
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
        verbose_name=_("Brand"),
        help_text=_("The brand this product belongs to. (Required)")
    )
    categories = TreeManyToManyField(
        "Category",
        related_name="products",
        blank=True,
        verbose_name=_("Categories"),
        help_text=_("The Categories this product belongs to. (Optional)")
    )
    type = models.ForeignKey(
        "ProductType",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Product Type"),
        help_text=_("The type of the product. (Required)")
    )
    sku = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("SKU"),
        help_text=_("Stock Keeping Unit - a unique identifier for the product. (Required)")
    )
    upc = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("UPC"),
        help_text=_("Universal Product Code - a unique identifier for the variant. (Optional)")
    )
    view_count = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name=_("View Count"),
        help_text=_("The number of times this product has been viewed. (Default: 0)")
    )
    is_recommend = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        verbose_name=_("Recommended Product"),
        help_text=_("Indicates if this product is recommended. (Default: No)")
    )
    is_featured = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        verbose_name=_("Featured Product"),
        help_text=_("Indicates if this product is featured. (Default: No)")
    )
    is_digital = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        verbose_name=_("Digital Product"),
        help_text=_("Indicates if this product is a digital product. (Default: No)")
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name=_("Product Visibility"),
        help_text=_("Controls whether the product is visible to customers. (Default: Visible)")
    )

    objects = ProductManager()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['is_active', 'is_featured']),
        ]
        ordering = ['created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('inventory:product_detail', kwargs={'slug': self.slug})

    def get_categories(self):
        return self.categories.order_by('order')

    def get_featured_image(self):
        return self.media.filter(is_featured=True).first()

    def get_default_variant(self):
        return self.variants.filter(is_default=True).first()

    def get_color_options(self):
        color_attr = Attribute.objects.filter(type=Attribute.AttributeTypeChoices.COLOR).first()
        if not color_attr:
            return []
        color_options = (
            self.variants.filter(is_active=True, attribute_values__attribute=color_attr)
            .values_list(
                "attribute_values__value_option__id",
                "attribute_values__value_option__value",
                "attribute_values__value_option__hex_code"
            )
            .distinct()
        )
        return [
            {
                "id": opt[0],
                "value": opt[1],
                "hex_code": opt[2]
            }
            for opt in color_options if opt[0] is not None
        ]

    def get_size_options(self):
        size_attr = Attribute.objects.filter(type=Attribute.AttributeTypeChoices.SIZE).first()
        if not size_attr:
            return []
        size_options = (
            self.variants.filter(is_active=True, attribute_values__attribute=size_attr)
            .values_list(
                "attribute_values__value_option__id",
                "attribute_values__value_option__value"
            )
            .distinct()
        )
        return [
            {
                "id": opt[0],
                "value": opt[1]
            }
            for opt in size_options if opt[0] is not None
        ]

    def get_attributes(self):
        attributes = self.type.attributes.all()
        attribute_values = self.attribute_values.select_related('attribute', 'value_option')

        result = []
        for attr in attributes:
            value = attribute_values.filter(attribute=attr).first()
            result.append({
                "attribute": {
                    "id": attr.id,
                    "name": attr.name,
                    "slug": attr.slug,
                    "type": attr.type,
                    "unit": attr.unit,
                    "is_required": attr.is_required,
                    "is_variant": attr.is_variant,
                    "is_filterable": attr.is_filterable,
                    "is_active": attr.is_active
                },
                "value": value.get_value() if value else None
            })
        return result

    def get_media(self):
        return self.media.filter(is_active=True).order_by('order')

    def get_variants(self):
        return self.variants.filter(is_active=True).order_by('name')

    def get_inventory(self):
        variant = self.get_default_variant()
        if variant and hasattr(variant, 'pricing'):
            return variant.inventory
        return None

    def get_pricing(self):
        variant = self.get_default_variant()
        if variant and hasattr(variant, 'pricing'):
            return variant.pricing
        return None


class ProductAttribute(TimeStampedModel):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="attribute_values",
        verbose_name=_("Product"),
        help_text=_("The product this attribute belongs to. (Required)")
    )
    attribute = models.ForeignKey(
        "Attribute",
        on_delete=models.CASCADE,
        # related_name="product_attributes",
        verbose_name=_("Attribute"),
        help_text=_("The attribute associated with this product. (Required)")
    )
    value_text = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Text Value"),
        help_text=_("Text value for the attribute. Used for Text type. (Optional)")
    )
    value_number = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Number Value"),
        help_text=_("Numeric value for the attribute. Used for Number type. (Optional)")
    )
    value_boolean = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_("Boolean Value"),
        help_text=_("Boolean value for the attribute. Used for Boolean type. (Optional)")
    )
    value_datetime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("DateTime Value"),
        help_text=_("DateTime value for the attribute. Used for DateTime type. (Optional)")
    )
    value_option = models.ForeignKey(
        "AttributeOption",
        on_delete=models.SET_NULL,
        related_name="product_attribute_values",
        null=True,
        blank=True,
        verbose_name=_("Option Value"),
        help_text=_("Selected option for the attribute. Used for Select, Color, Size types. (Optional)")
    )

    class Meta:
        verbose_name = _("Product Attribute")
        verbose_name_plural = _("Product Attributes")
        unique_together = ('product', 'attribute')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}"

    def get_value(self):
        attr_type = self.attribute.type
        if attr_type == self.attribute.AttributeTypeChoices.TEXT:
            return self.value_text
        elif attr_type == self.attribute.AttributeTypeChoices.NUMBER:
            return self.value_number
        elif attr_type == self.attribute.AttributeTypeChoices.BOOLEAN:
            return self.value_boolean
        elif attr_type == self.attribute.AttributeTypeChoices.DATETIME:
            return self.value_datetime
        elif attr_type in [self.attribute.AttributeTypeChoices.SELECT, self.attribute.AttributeTypeChoices.COLOR, self.attribute.AttributeTypeChoices.SIZE]:
            return self.value_option
        else:
            return self.value_text


class ProductVariant(TimeStampedModel):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="variants",
        verbose_name=_("Product"),
        help_text=_("The product this variant belongs to. (Required)")
    )
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name=_("Variant Name"),
        help_text=_("The name of the product variant. (Required)")
    )
    sku = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("SKU"),
        help_text=_("Stock Keeping Unit - a unique identifier for the variant. (Required)")
    )
    upc = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("UPC"),
        help_text=_("Universal Product Code - a unique identifier for the variant. (Optional)")
    )
    is_default = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        verbose_name=_("Default Variant"),
        help_text=_("Indicates if this is the default variant for the product. (Default: No)")
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name=_("Variant Visibility"),
        help_text=_("Controls whether the variant is visible to customers. (Default: Visible)")
    )

    # Physical properties
    # weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    # length = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    # width = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    # height = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _("Product Variant")
        verbose_name_plural = _("Product Variants")
        unique_together = ['product', 'name']
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['product', 'is_active']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    def save(self, *args, **kwargs):
        # Ensure only one default variant per product
        if self.is_default:
            ProductVariant.objects.filter(
                product=self.product,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)

        super().save(*args, **kwargs)

        # Ensure at least one default variant exists for the product
        if not self.is_default and not ProductVariant.objects.filter(product=self.product, is_default=True).exists():
            if self.pk:
                self.is_default = True
                ProductVariant.objects.filter(pk=self.pk).update(is_default=True)


class ProductVariantAttribute(TimeStampedModel):
    variant = models.ForeignKey(
        "ProductVariant",
        on_delete=models.CASCADE,
        related_name="attribute_values",
        verbose_name=_("Product Variant"),
        help_text=_("The product variant this attribute belongs to. (Required)")
    )
    attribute = models.ForeignKey(
        "Attribute",
        on_delete=models.CASCADE,
        # related_name="variant_attributes",
        verbose_name=_("Attribute"),
        help_text=_("The attribute associated with this variant. (Required)")
    )
    value_text = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Text Value"),
        help_text=_("Text value for the attribute. Used for Text type. (Optional)")
    )
    value_number = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Number Value"),
        help_text=_("Numeric value for the attribute. Used for Number type. (Optional)")
    )
    value_boolean = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_("Boolean Value"),
        help_text=_("Boolean value for the attribute. Used for Boolean type. (Optional)")
    )
    value_datetime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("DateTime Value"),
        help_text=_("DateTime value for the attribute. Used for DateTime type. (Optional)")
    )
    value_option = models.ForeignKey(
        "AttributeOption",
        on_delete=models.SET_NULL,
        related_name="variant_attribute_values",
        null=True,
        blank=True,
        verbose_name=_("Option Value"),
        help_text=_("Selected option for the attribute. Used for Select, Color, Size types. (Optional)")
    )

    class Meta:
        verbose_name = _("Product Variant Attribute")
        verbose_name_plural = _("Product Variant Attributes")
        unique_together = ('variant', 'attribute')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.variant.name} - {self.attribute.name}"

    def get_value(self):
        attr_type = self.attribute.type
        if attr_type == self.attribute.AttributeTypeChoices.TEXT:
            return self.value_text
        elif attr_type == self.attribute.AttributeTypeChoices.NUMBER:
            return self.value_number
        elif attr_type == self.attribute.AttributeTypeChoices.BOOLEAN:
            return self.value_boolean
        elif attr_type == self.attribute.AttributeTypeChoices.DATETIME:
            return self.value_datetime
        elif attr_type in [self.attribute.AttributeTypeChoices.SELECT, self.attribute.AttributeTypeChoices.COLOR, self.attribute.AttributeTypeChoices.SIZE]:
            return self.value_option
        else:
            return self.value_text


class ProductMedia(TimeStampedModel):
    class ProductMediaTypeChoices(models.TextChoices):
        IMAGE = 'image', _("Image")
        VIDEO = 'video', _("Video")
        DOCUMENT = 'document', _("Document")

    def media_path(instance, filename):
        return generate_upload_path(instance, filename, prefix='uploads/products/media', field_name=f"media_{instance.product.name}")

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="media",
        verbose_name=_("Product"),
        help_text=_("The product this media belongs to. (Required)")
    )
    variant = models.ForeignKey(
        "ProductVariant",
        on_delete=models.CASCADE,
        related_name='media',
        null=True,
        blank=True
    )
    type = models.CharField(
        max_length=10,
        choices=ProductMediaTypeChoices.choices,
        default=ProductMediaTypeChoices.IMAGE,
        null=False,
        blank=False,
        verbose_name=_("Media Type"),
        help_text=_("The type of media: image or video. (Default: Image)")
    )
    file = models.FileField(
        upload_to=media_path,
        null=True,
        blank=True,
        verbose_name=_("Media File"),
        help_text=_("The media file (image or video) associated with the product. (Optional)")
    )
    alt_text = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Alternative Text"),
        help_text=_("Alternative text for the media file, used for accessibility. (Optional)")
    )
    is_featured = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        verbose_name=_("Featured Media"),
        help_text=_("Indicates if this media is featured for the product. (Default: No)")
    )
    order = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name=_("Order"),
        help_text=_("The order in which media is displayed. Lower numbers appear first. (Default: 0)")
    )

    class Meta:
        verbose_name = _("Product Media")
        verbose_name_plural = _("Product Media")
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['product', 'is_featured']),
            models.Index(fields=['variant', 'type']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.type}"

    def save(self, *args, **kwargs):
        # Ensure only one featured media per product
        if self.is_featured:
            ProductMedia.objects.filter(
                product=self.product,
                is_featured=True
            ).exclude(pk=self.pk).update(is_featured=False)
        super().save(*args, **kwargs)

    def get_file_url(self):
        if self.file:
            return self.file.url
        return static('assets/images/placeholders/product_media.webp')


class Inventory(TimeStampedModel):
    variant = models.OneToOneField(
        "ProductVariant",
        on_delete=models.CASCADE,
        related_name='inventory',
        null=False,
        blank=False,
        verbose_name=_("Product Variant"),
        help_text=_("The product variant this inventory record belongs to. (Required)")
    )
    quantity = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name=_("Quantity"),
        help_text=_("The available stock quantity for the product or variant. (Default: 0)")
    )
    reserved_quantity = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name=_("Reserved Quantity"),
        help_text=_("The quantity reserved for pending orders. (Default: 0)")
    )
    reorder_level = models.PositiveIntegerField(
        default=5,
        null=False,
        blank=False,
        verbose_name=_("Reorder Level"),
        help_text=_("The stock level at which a reorder should be triggered. (Default: 5)")
    )
    track_quantity = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name=_("Track Quantity"),
        help_text=_("Indicates if the inventory quantity should be tracked. (Default: Yes)")
    )
    allow_backorders = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        verbose_name=_("Allow Backorders"),
        help_text=_("Indicates if backorders are allowed when stock is insufficient. (Default: No)")
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name=_("Inventory Visibility"),
        help_text=_("Controls whether the inventory record is active. (Default: Active)")
    )

    class Meta:
        verbose_name = _("Inventory")
        verbose_name_plural = _("Inventories")
        # unique_together = ('product', 'variant')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.variant.name} - Stock: {self.quantity}"

    @property
    def available_quantity(self):
        return max(0, self.quantity - self.reserved_quantity)

    @property
    def is_in_stock(self):
        if not self.track_quantity:
            return True
        return self.available_quantity > 0 or self.allow_backorders

    def has_enough_quantity(self, quantity):
        if not self.track_quantity:
            return True

        if self.available_quantity >= quantity:
            return True

        return self.allow_backorders


class Pricing(TimeStampedModel):
    class CurrencyChoices(models.TextChoices):
        USD = 'USD', _("US Dollar")
        EUR = 'EUR', _("Euro")
        GBP = 'GBP', _("British Pound")
        JPY = 'JPY', _("Japanese Yen")
        CNY = 'CNY', _("Chinese Yuan")
        CAD = 'CAD', _("Canadian Dollar")
        AUD = 'AUD', _("Australian Dollar")
        INR = 'INR', _("Indian Rupee")

    variant = models.OneToOneField(
        "ProductVariant",
        on_delete=models.CASCADE,
        related_name='pricing',
        null=False,
        blank=False,
        verbose_name=_("Product Variant"),
        help_text=_("The product variant this pricing belongs to. (Required)")
    )
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name=_("Cost Price"),
        help_text=_("The cost price of the inventory item. (Optional)")
    )
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        validators=[MinValueValidator(0)],
        verbose_name=_("Base Price"),
        help_text=_("The base price of the inventory item before any discounts or sales. (Required)")
    )
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name=_("Sale Price"),
        help_text=_("The sale price of the inventory item. If set, this overrides the base price. (Optional)")
    )
    sale_start_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Sale Start Date"),
        help_text=_("The date and time when the sale price starts. (Optional)")
    )
    sale_end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Sale End Date"),
        help_text=_("The date and time when the sale price ends. (Optional)")
    )
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.USD,
        null=False,
        blank=False,
        verbose_name=_("Currency"),
        help_text=_("The currency for the price.")
    )

    class Meta:
        verbose_name = _("Pricing")
        verbose_name_plural = _("Pricing")
        unique_together = ['variant', 'currency']
        indexes = [
            models.Index(fields=['variant']),
            models.Index(fields=['sale_start_date', 'sale_end_date']),
        ]

    def __str__(self):
        return f"{self.variant.name} - {self.currency}"

    @property
    def current_price(self):
        now = timezone.now()

        if self.sale_price and (not self.sale_start_date or self.sale_start_date <= now) and (not self.sale_end_date or self.sale_end_date >= now):
            return self.sale_price
        return self.base_price

    @property
    def is_on_sale(self):
        return self.current_price != self.base_price

    @property
    def is_free(self):
        return self.current_price <= 0

    @property
    def saved_amount(self):
        if self.is_on_sale:
            return self.base_price - self.current_price
        return 0

# Todo ProductReview
# class ProductReview

# class PricingTier(TimeStampedModel):
#     name = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True,
#         verbose_name=_("Tier Name"),
#         help_text=_("Optional name for the pricing tier. (Optional)")
#     )
#     description = models.TextField(
#         null=True,
#         blank=True,
#         verbose_name=_("Tier Description"),
#         help_text=_("Optional description for the pricing tier. (Optional)")
#     )
#     is_default = models.BooleanField(
#         default=False,
#         null=False,
#         blank=False,
#         verbose_name=_("Default Tier"),
#         help_text=_("Indicates if this is the default pricing tier for the inventory. (Default: No)")
#     )
#
#     class Meta:
#         verbose_name = _("Pricing Tier")
#         verbose_name_plural = _("Pricing Tiers")
#         ordering = ['created_at']
#
#     def __str__(self):
#         return self.name
#
#     def save(self, *args, **kwargs):
#         # Ensure only one default tier
#         if self.is_default:
#             PricingTier.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)
#         super().save(*args, **kwargs)

# class Pricing(TimeStampedModel):
#     class CurrencyChoices(models.TextChoices):
#         USD = 'USD', _("US Dollar")
#         EUR = 'EUR', _("Euro")
#         GBP = 'GBP', _("British Pound")
#         JPY = 'JPY', _("Japanese Yen")
#         CNY = 'CNY', _("Chinese Yuan")
#         CAD = 'CAD', _("Canadian Dollar")
#         AUD = 'AUD', _("Australian Dollar")
#         INR = 'INR', _("Indian Rupee")
#
#     variant = models.ForeignKey(
#         "ProductVariant",
#         on_delete=models.CASCADE,
#         related_name='pricing',
#         null=True,
#         blank=True,
#         verbose_name=_("Product Variant"),
#         help_text=_("The product variant this pricing belongs to. (Required)")
#     )
#     tier = models.ForeignKey(
#         "PricingTier",
#         on_delete=models.CASCADE,
#         related_name='pricing',
#         null=True,
#         blank=True,
#         verbose_name=_("Pricing Tier"),
#         help_text=_("The pricing tier this pricing belongs to. (Optional)")
#     )
#     cost_price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         validators=[MinValueValidator(0)],
#         verbose_name=_("Cost Price"),
#         help_text=_("The cost price of the inventory item. (Optional)")
#     )
#     base_price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         validators=[MinValueValidator(0)],
#         verbose_name=_("Base Price"),
#         help_text=_("The base price of the inventory item before any discounts or sales. (Optional)")
#     )
#     sale_price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         validators=[MinValueValidator(0)],
#         verbose_name=_("Sale Price"),
#         help_text=_("The sale price of the inventory item. If set, this overrides the base price. (Optional)")
#     )
#     sale_start_date = models.DateTimeField(
#         null=True,
#         blank=True,
#         verbose_name=_("Sale Start Date"),
#         help_text=_("The date and time when the sale price starts. (Optional)")
#     )
#     sale_end_date = models.DateTimeField(
#         null=True,
#         blank=True,
#         verbose_name=_("Sale End Date"),
#         help_text=_("The date and time when the sale price ends. (Optional)")
#     )
#     currency = models.CharField(
#         max_length=3,
#         choices=CurrencyChoices.choices,
#         default=CurrencyChoices.USD,
#         null=False,
#         blank=False,
#         verbose_name=_("Currency"),
#         help_text=_("The currency for the price.")
#     )
#
#     class Meta:
#         verbose_name = _("Pricing")
#         verbose_name_plural = _("Pricing")
#         unique_together = ['variant', 'tier']
#         indexes = [
#             models.Index(fields=['variant', 'tier']),
#             # models.Index(fields=['sale_start_date', 'sale_end_date']),
#         ]
#
#     def __str__(self):
#         return f"{self.variant.name} - {self.tier.name}"
#
#     @property
#     def current_price(self):
#         """Get current effective price"""
#         from django.utils import timezone
#         now = timezone.now()
#
#         # Check if sale price is active
#         if self.sale_price and (not self.sale_start_date or self.sale_start_date <= now) and (not self.sale_end_date or self.sale_end_date >= now):
#             return self.sale_price
#
#         return self.base_price
#
#     @property
#     def is_on_sale(self):
#         """Check if the product is currently on sale"""
#         return self.current_price != self.base_price
