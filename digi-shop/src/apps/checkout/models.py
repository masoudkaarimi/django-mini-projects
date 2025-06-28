from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel


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

# class Order
# class OrderItem
# class Payment
# class Currency
# Shipping or Delivery

# Promotion App
# class Promotion
# class PromotionType
# class Coupon
# class ProductsOnPromotion

# Settings App
# class Settings
# class EmailTemplate
# class Page
# class SeoPage
# class BannerPage

# Analytics App


# OTP
# ورود ثبت نام با OTP
# ثبت‌نام و ورود با شماره تلفن:
# ثبت‌نام با شماره تلفن:
# اگر شماره تلفن قبلا ثبت نشده باشد، ثبت‌نام موقت انجام شده و کد تأیید ارسال می‌گردد.
# پس از ارسال کد تأیید و صحت‌سنجی آن، ثبت نام نهایی صورت می‌گیرد و کاربر به بخش تکمیل پروفایل هدایت می‌شود.
# ورود با شماره تلفن:
# اگر شماره تلفن وجود داشته باشد، کد تأیید ارسال شده و پس از تأیید کد، کاربر وارد سیستم می‌شود.
# ثبت‌نام و ورود با ایمیل:
# ثبت‌نام با ایمیل:
# اگر ایمیل وجود نداشته باشد، ثبت‌نام با شماره تلفن صورت می‌گیرد.
# ورود با ایمیل:
# اگر ایمیل وجود داشته باشد، ورود فقط با استفاده از رمز عبور امکان‌پذیر است.
# ارسال مجدد کد تأیید با شماره تلفن:
# در صورتی که کد تأیید دریافت نشود، کاربر می‌تواند پس از دو دقیقه، درخواست ارسال مجدد کد داشته باشد. با فشار دادن دکمه "ارسال مجدد"، کد تأیید جدیدی به شماره تلفن ارسال خواهد شد.
# تکمیل پروفایل:
# پس از تکمیل ثبت‌نام، صفحه‌ای برای تکمیل پروفایل و تنظیم رمز عبور نمایش داده می‌شود.
# ورود با رمز عبور:
# اگر کاربر رمز عبور را قبلاً تنظیم کرده باشد، می‌تواند با استفاده از ایمیل یا شماره تلفن خود و رمز عبور وارد سیستم شود.
# فراموشی رمز عبور:
# با ایمیل:
# اگر کاربر ایمیل خود را وارد کند، لینک تغییر رمز عبور که شامل یک توکن است، به ایمیل ارسال می‌شود. این لینک پس از 48 ساعت منقضی می‌گردد و به وسیله آن کاربر می‌تواند رمز عبور جدیدی برای خود تنظیم کند.
# با شماره تلفن:
# اگر کاربر شماره تلفن خود را وارد کند، کد تأیید برای او ارسال می‌شود. پس از ارسال کد تأیید و صحت‌سنجی آن، یک توکن ارسال می‌شود که به کاربر اجازه می‌دهد رمز عبور جدیدی برای خود تنظیم کند.
