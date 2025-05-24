from django.db import models
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey, TreeManyToManyField


class Brand(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Brand Name"),
        help_text=_("Format: required, max-255 characters"),
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Brand Slug"),
        help_text=_("Format: required, max-255 letters, numbers, underscores, or hyphens"),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Brand Description"),
        help_text=_("Format: optional, max-5000 characters")
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name=_("Brand Visibility"),
        help_text=_("Format: optional, default=True"),
    )

    class Meta:
        ordering = ['name']
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.name


class Category(MPTTModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Category Name"),
        help_text=_("Format: required, max-255 characters"),
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Category Slug"),
        help_text=_("Format: required, max-255 letters, numbers, underscores, or hyphens"),
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        unique=False,
        null=True,
        blank=True,
        verbose_name=_("Parent Category"),
        help_text=_("Format: optional"),
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name=_("Category Visibility"),
        help_text=_("Format: optional, default=True"),
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        ordering = ['name']
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Product Type Name"),
        help_text=_("Format: required, max-255 characters"),
    )

    class Meta:
        ordering = ['name']
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Product Attribute Name"),
        help_text=_("Format: required, max-255 characters"),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Product Attribute Description"),
        help_text=_("Format: optional, max-5000 characters")
    )

    class Meta:
        ordering = ['name']
        verbose_name = _("Product Attribute")
        verbose_name_plural = _("Product Attributes")

    def __str__(self):
        return self.name


class ProductTypeAttribute(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        related_name='product_type_attributes',
        on_delete=models.PROTECT,
        verbose_name=_("Product Type"),
        help_text=_("Format: required")
    )
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name='product_type_attributes',
        on_delete=models.PROTECT,
        verbose_name=_("Product Attribute"),
        help_text=_("Format: required")
    )

    class Meta:
        unique_together = ('product_type', 'product_attribute')
        verbose_name = _("Product Type Attribute")
        verbose_name_plural = _("Product Type Attributes")

    def __str__(self):
        return f"{self.product_type.name} - {self.product_attribute.name}"


class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="attribute_values",
        on_delete=models.PROTECT,
        verbose_name=_("Product Attribute"),
        help_text=_("Format: required")
    )
    value = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name=_("Product Attribute Value"),
        help_text=_("Format: required, max-255 characters")
    )

    class Meta:
        unique_together = ('product_attribute', 'value')
        verbose_name = _("Product Attribute Value")
        verbose_name_plural = _("Product Attribute Values")

    def __str__(self):
        return f"{self.product_attribute.name}: {self.value}"


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Product Name"),
        help_text=_("Format: required, max-255 characters"),
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Product Slug"),
        help_text=_("Format: required, max-255 letters, numbers, underscores, or hyphens"),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Product Description"),
        help_text=_("Format: optional, max-5000 characters")
    )
    category = TreeManyToManyField(
        Category,
        related_name="category_products",
        null=True,
        blank=True,
        verbose_name=_("Category"),
        help_text=_("Format: optional")
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name=_("Product Visibility"),
        help_text=_("Format: optional, default=True"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Date Created"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date Last Updated"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    class Meta:
        ordering = ['name']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name


class ProductInventoryManager(models.Manager):
    def get_filtered_products(self, slug, filters):
        return (self.filter(product__slug=slug)
                .filter(attribute_values__in=filters)
                .annotate(num_filters=Count("attribute_values"))
                .filter(num_filters=len(filters))
                .values("id", "sku", "product__name", "store_price", "stock__units")
                .annotate(attribute_values_list=ArrayAgg("attribute_values")))

    def get_default_product(self, slug):
        return (self.filter(product__slug=slug)
                .filter(is_default=True)
                .values("id", "sku", "product__name", "store_price", "stock__units")
                .annotate(attribute_values_list=ArrayAgg("attribute_values")).get())

    def get_attribute_values(self, slug):
        return self.filter(product__slug=slug).distinct().values(
            "attribute_values__product_attribute__name",
            "attribute_values__value"
        )


class ProductInventory(models.Model):
    sku = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("SKU (Stock Keeping Unit)"),
        help_text=_("Format: required, max-50 characters, unique identifier for the product")
    )
    upc = models.CharField(
        max_length=12,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("UPC (Universal Product Code)"),
        help_text=_("Format: optional, max-12 characters, unique identifier for the product")
    )
    product = models.ForeignKey(
        Product,
        related_name="inventory",
        on_delete=models.PROTECT,
        verbose_name=_("Product"),
        help_text=_("Format: required")
    )
    product_type = models.ForeignKey(
        ProductType,
        related_name="product_type_inventories",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Product Type"),
        help_text=_("Format: optional, select the product type for this inventory")
    )
    brand = models.ForeignKey(
        Brand,
        related_name="brand_inventories",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Brand"),
        help_text=_("Format: optional, select the brand for this inventory")
    )
    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        related_name="product_inventories",
        through="ProductInventoryAttributeValue",
        blank=True,
        verbose_name=_("Product Attribute Values"),
        help_text=_("Format: optional, select attribute values applicable to this inventory")
    )
    retail_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        verbose_name=_("Retail Price"),
        help_text=_("Format: required, must be a positive decimal number, e.g., 19.99"),
    )
    store_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        verbose_name=_("Store Price"),
        help_text=_("Format: optional, must be a positive decimal number, e.g., 19.99"),
    )
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        verbose_name=_("Sale Price"),
        help_text=_("Format: optional, must be a positive decimal number, e.g., 19.99"),
    )
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Weight"),
        help_text=_("Format: optional, must be a positive decimal number, e.g., 1.5"),
    )
    is_default = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        verbose_name=_("Default Inventory"),
        help_text=_("Format: optional, default=False, indicates if this is the default inventory for the product"),
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name=_("Inventory Visibility"),
        help_text=_("Format: optional, default=True"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Date Created"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date Last Updated"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    objects = ProductInventoryManager()

    class Meta:
        ordering = ['product__name', 'sku']
        verbose_name = _("Product Inventory")
        verbose_name_plural = _("Product Inventories")

    def __str__(self):
        return self.product.name


class ProductInventoryAttributeValue(models.Model):
    product_inventory = models.ForeignKey(
        ProductInventory,
        related_name='product_attribute_values',
        on_delete=models.PROTECT,
        verbose_name=_("Product Inventory"),
        help_text=_("Format: required")
    )
    attribute_value = models.ForeignKey(
        ProductAttributeValue,
        related_name='inventory_attribute_values',
        on_delete=models.PROTECT,
        verbose_name=_("Product Attribute Value"),
        help_text=_("Format: required")
    )

    class Meta:
        unique_together = ('product_inventory', 'attribute_value')
        verbose_name = _("Product Inventory Attribute Value")
        verbose_name_plural = _("Product Inventory Attribute Values")

    def __str__(self):
        return f"{self.product_inventory.product.name} - {self.attribute_value.value}"


class Stock(models.Model):
    product_inventory = models.OneToOneField(
        ProductInventory,
        on_delete=models.PROTECT,
        related_name="stock",
        verbose_name=_("Product Inventory"),
        help_text=_("Format: required")
    )
    units = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name=_("Units in Stock"),
        help_text=_("Format: required, must be a positive integer"),
    )
    units_sold = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name=_("Units Sold"),
        help_text=_("Format: required, must be a positive integer"),
    )
    last_checked = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Inventory Stock Last Checked"),
        help_text=_("Format: Y-m-d H:M:S"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Date Stock Created"),
        help_text=_("Format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date Stock Updated"),
        help_text=_("Format: Y-m-d H:M:S"),
    )

    class Meta:
        verbose_name = _("Product Stock")
        verbose_name_plural = _("Product Stocks")

    def __str__(self):
        return f"{self.product_inventory.product.name} - {self.units} units"


class Media(models.Model):
    product_inventory = models.ForeignKey(
        ProductInventory,
        related_name="media",
        on_delete=models.CASCADE,
        verbose_name=_("Product Inventory"),
        help_text=_("Format: required")
    )
    image = models.ImageField(
        upload_to='images/products/',
        default="images/products/default.png",
        null=True,
        blank=True,
        verbose_name=_("Product Image"),
        help_text=_("Format: optional")
    )
    alt_text = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Image Alt Text"),
        help_text=_("Format: optional, max-255 characters, used for accessibility and SEO")
    )
    is_featured = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        verbose_name=_("Featured Image"),
        help_text=_("Format: optional, default=False, indicates if this image is featured for the product")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Date Created"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date Last Updated"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    class Meta:
        ordering = ['-is_featured', 'created_at']
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return f"{self.product_inventory.product.name} - {self.alt_text or 'No Alt Text'}"
