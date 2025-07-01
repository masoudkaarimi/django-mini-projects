from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from apps.common.models import TimeStampedModel


class OrderManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(user=user)

    def pending(self):
        return self.get_queryset().filter(status=Order.OrderStatusChoices.PENDING)

    def confirmed(self):
        return self.get_queryset().filter(status=Order.OrderStatusChoices.CONFIRMED)

    def processing(self):
        return self.get_queryset().filter(status=Order.OrderStatusChoices.PROCESSING)

    def shipped(self):
        return self.get_queryset().filter(status=Order.OrderStatusChoices.SHIPPED)

    def delivered(self):
        return self.get_queryset().filter(status=Order.OrderStatusChoices.DELIVERED)

    def cancelled(self):
        return self.get_queryset().filter(status=Order.OrderStatusChoices.CANCELLED)

    def refunded(self):
        return self.get_queryset().filter(status=Order.OrderStatusChoices.REFUNDED)


class Cart(TimeStampedModel):
    user = models.OneToOneField(
        "account.User",
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name=_('User'),
        help_text=_('The user who owns this cart.')
    )

    # notes = models.TextField(
    #     null=True,
    #     blank=True,
    #     verbose_name=_('Cart Notes'),
    #     help_text=_('Additional notes for this cart.')
    # )

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email}'s Cart"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def item_count(self):
        return self.items.count()

    def clear(self):
        self.items.all().delete()
        return True


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(
        "Cart",
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Cart'),
        help_text=_('The cart this item belongs to.')
    )
    product_variant = models.ForeignKey(
        'inventory.ProductVariant',
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name=_('Product Variant'),
        help_text=_('The product variant in the cart.')
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Quantity'),
        help_text=_('Quantity of the product in the cart.')
    )
    reserved_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Reserved Until'),
        help_text=_('Time until the inventory is reserved for this cart item.')
    )

    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')
        unique_together = ('cart', 'product_variant')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.quantity} × {self.product_variant.name}"

    @property
    def subtotal(self):
        if hasattr(self.product_variant, 'pricing'):
            return self.product_variant.pricing.current_price * self.quantity
        return 0

    def reserve(self, minutes=15):
        self.reserved_until = timezone.now() + timezone.timedelta(minutes=minutes)
        self.save(update_fields=['reserved_until'])
        return self.reserved_until

    def is_reservation_valid(self):
        if not self.reserved_until:
            return False
        return timezone.now() <= self.reserved_until


class Order(TimeStampedModel):
    class OrderStatusChoices(models.TextChoices):
        PENDING = 'pending', _("Order in progress")
        CONFIRMED = 'confirmed', _("Confirmed")
        PROCESSING = 'processing', _("Preparing order")
        SHIPPED = 'shipped', _("Shipped")
        DELIVERED = 'delivered', _("Order delivered")
        CANCELLED = 'cancelled', _("Cancelled")
        REFUNDED = 'refunded', _("Refunded")

    objects = OrderManager()

    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("User"),
        help_text=_("The user who placed the order. (Required)")
    )
    order_number = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Order Number"),
        help_text=_("Unique order number for tracking. Auto-generated if not provided. (Required)")
    )
    cart = models.OneToOneField(
        Cart,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order',
        verbose_name=_('Cart'),
        help_text=_('The cart associated with this order.')
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PENDING,
        null=False,
        blank=False,
        verbose_name=_("Order Status"),
        help_text=_("Current status of the order. (Default: Pending)")
    )
    contact_email = models.EmailField(
        verbose_name=_("Contact Email"),
        help_text=_("Email address for order communications.")
    )
    contact_phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_("Contact Phone"),
        help_text=_("Phone number for order communications.")
    )
    shipping_address_country = CountryField(
        blank=False,
        null=False,
        blank_label=_('(select country)'),
        verbose_name=_("Country/Region"),
        help_text=_("The country or region of the address. (Required)")
    )
    shipping_address_city = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name=_("City"),
        help_text=_("The city of the address. (Required)")
    )
    shipping_address_state = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name=_("State/Province"),
        help_text=_("The state or province of the address. (Required)")
    )
    shipping_address_zip_code = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        verbose_name=_("Zip/Postal Code"),
        help_text=_("The zip or postal code of the address. (Required)")
    )
    shipping_address_address_line_1 = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name=_("Address Line 1"),
        help_text=_("Additional address line, e.g., apartment or suite number. (Optional)")
    )
    shipping_address_address_line_2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Address Line 2"),
        help_text=_("Additional address line, e.g., building or floor number. (Optional)")
    )
    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Shipping Cost'),
        help_text=_('Cost of shipping for this order.')
    )
    tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Tax Amount'),
        help_text=_('Tax amount for this order.')
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Discount Amount'),
        help_text=_('Discount applied to this order.')
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Subtotal'),
        help_text=_('Order subtotal before tax and shipping.')
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Total Amount'),
        help_text=_('Final total amount for the order.')
    )
    currency = models.CharField(
        max_length=3,
        default="USD",
        verbose_name=_("Currency"),
        help_text=_("Currency code for the order (e.g., USD, EUR).")
    )
    estimated_delivery = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Estimated Delivery"),
        help_text=_("Estimated delivery date for this order.")
    )
    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Order Notes'),
        help_text=_('Additional notes for this order.')
    )

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number} by {self.user.email}"

    def save(self, *args, **kwargs):
        # Generate order number if not provided
        if not self.order_number:
            prefix = "ORD"
            timestamp = int(timezone.now().timestamp())
            self.order_number = f"{prefix}{timestamp}"

        # Calculate total if not set
        if not self.total:
            self.total = self.subtotal + self.shipping_cost + self.tax_amount - self.discount

        super().save(*args, **kwargs)

    @property
    def is_cancelable(self):
        """Check if the order can be canceled based on its status."""
        return self.status in [
            self.OrderStatusChoices.PENDING,
            self.OrderStatusChoices.CONFIRMED
        ]

    def cancel(self):
        """Cancel the order if it's in a cancelable state."""
        if self.is_cancelable:
            self.status = self.OrderStatusChoices.CANCELLED
            self.save(update_fields=['status'])
            return True
        return False

    def get_receipt_url(self):
        """Get URL to the receipt/invoice for this order."""
        # Implementation would depend on your PDF/receipt generation system
        return f"/orders/{self.order_number}/receipt/"


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Order'),
        help_text=_('The order this item belongs to.')
    )
    product_variant = models.ForeignKey(
        'inventory.ProductVariant',
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name=_('Product Variant'),
        help_text=_('The product variant in the order.')
    )
    product_name = models.CharField(
        max_length=255,
        verbose_name=_('Product Name'),
        help_text=_('Name of the product at the time of order.')
    )
    color = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('Color'),
        help_text=_('Color of the product variant.')
    )
    size = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('Size'),
        help_text=_('Size of the product variant.')
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Quantity'),
        help_text=_('Quantity of the product in the order.')
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Unit Price'),
        help_text=_('Price per unit of the product variant at the time of order.')
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Subtotal'),
        help_text=_('Subtotal for this item (quantity × unit price).')
    )
    image_url = models.URLField(
        null=True,
        blank=True,
        verbose_name=_('Product Image URL'),
        help_text=_('URL to the image of the product.')
    )

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.quantity} × {self.product_name} in Order #{self.order.order_number}"

    def save(self, *args, **kwargs):
        # Calculate subtotal automatically
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class Payment(TimeStampedModel):
    class PaymentMethodChoices(models.TextChoices):
        MASTERCARD = 'mastercard', _("MasterCard")
        VISA = 'visa', _("Visa")
        PAYPAL = 'paypal', _("PayPal")
        COD = 'cod', _("Cash on Delivery")

    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', _("Pending")
        PROCESSING = 'processing', _("Processing")
        PAID = 'paid', _("Paid")
        FAILED = 'failed', _("Failed")
        REFUNDED = 'refunded', _("Refunded")

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name=_('Order'),
        help_text=_('The order associated with this payment.')
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Amount'),
        help_text=_('Amount paid for the order.')
    )
    method = models.CharField(
        max_length=20,
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.COD,
        verbose_name=_("Payment Method"),
        help_text=_("Method used for payment.")
    )
    status = models.CharField(
        max_length=20,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING,
        verbose_name=_("Payment Status"),
        help_text=_("Current status of the payment.")
    )
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Transaction ID"),
        help_text=_("Unique identifier for the payment transaction.")
    )
    payment_intent = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        verbose_name=_("Payment Intent"),
        help_text=_("Payment processor intent ID (e.g., Stripe payment_intent).")
    )
    currency = models.CharField(
        max_length=3,
        default="USD",
        verbose_name=_("Currency"),
        help_text=_("Currency code for the payment (e.g., USD, EUR).")
    )
    card_last4 = models.CharField(
        max_length=4,
        null=True,
        blank=True,
        verbose_name=_("Last 4 Digits"),
        help_text=_("Last 4 digits of the payment card.")
    )
    card_expiry = models.CharField(
        max_length=5,
        null=True,
        blank=True,
        verbose_name=_("Card Expiry"),
        help_text=_("Expiration date of the payment card (MM/YY).")
    )
    cardholder_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Cardholder Name"),
        help_text=_("Name of the cardholder.")
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name=_("Default Payment Method"),
        help_text=_("Whether this is the default payment method for the user.")
    )

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment for Order #{self.order.order_number} - {self.status}"

    def masked_card(self):
        """Return masked card number representation."""
        if self.card_last4:
            return f"•••• •••• •••• {self.card_last4}"
        return ""


class Delivery(TimeStampedModel):
    name = models.CharField(
        max_length=100,
        default=_('Standard Delivery'),
        verbose_name=_('Delivery Name'),
        help_text=_('Name of the delivery service or method. (Required)'),
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='delivery',
        verbose_name=_('Order'),
        help_text=_('The order associated with this delivery.')
    )
    address = models.ForeignKey(
        "account.Address",
        on_delete=models.PROTECT,
        related_name='deliveries',
        verbose_name=_('Delivery Address'),
        help_text=_('Address where the order will be delivered.')
    )
    tracking_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('Tracking Number'),
        help_text=_('Delivery tracking number if available.')
    )
    carrier = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('Shipping Carrier'),
        help_text=_('Name of the shipping carrier (e.g., UPS, FedEx).')
    )
    estimated_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Estimated Delivery Date'),
        help_text=_('Estimated date for delivery.')
    )
    actual_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Actual Delivery Date'),
        help_text=_('Actual date and time of delivery.')
    )
    status = models.CharField(
        max_length=20,
        choices=Order.OrderStatusChoices.choices,
        default=Order.OrderStatusChoices.PENDING,
        verbose_name=_("Delivery Status"),
        help_text=_("Current status of the delivery.")
    )
    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Delivery Notes'),
        help_text=_('Additional notes for this delivery.')
    )

    class Meta:
        verbose_name = _('Delivery')
        verbose_name_plural = _('Deliveries')
        ordering = ['-created_at']

    def __str__(self):
        return f"Delivery for Order #{self.order.order_number} to {self.address}"
