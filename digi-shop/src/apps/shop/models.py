from django.db import models
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel
from apps.common.utils import generate_upload_path


class SliderBanner(TimeStampedModel):
    def banner_path(instance, filename):
        return generate_upload_path(instance, filename, prefix='uploads/slider_banners', field_name=f"banner_{instance.title or 'untitled'}")

    title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_("Banner Title"),
        help_text=_("Optional title shown on the banner.")
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("Banner Slug"),
        help_text=_("URL-friendly identifier for this banner. Must be unique.")
    )
    subtitle = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Banner Subtitle"),
        help_text=_("Optional subtitle or description shown on the banner.")
    )
    image = models.ImageField(
        upload_to=banner_path,
        null=False,
        blank=False,
        verbose_name=_("Banner Image"),
        help_text=_("Image displayed in the slider banner.")
    )
    link_url = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name=_("Link URL"),
        help_text=_("Optional URL to navigate to when the banner is clicked.")
    )
    order = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name=_("Display Order"),
        help_text=_("Controls the order banners are displayed in the slider.")
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name=_("Banner Visibility"),
        help_text=_("Determines if the banner is visible on the site.")
    )

    class Meta:
        verbose_name = _("Slider Banner")
        verbose_name_plural = _("Slider Banners")
        ordering = ['order', 'title']

    def __str__(self):
        return self.title or f"Banner #{self.pk}"

    def get_image_url(self):
        if self.image:
            return self.image.url
        return static('assets/images/placeholders/banner-placeholder.webp')


class FAQ(TimeStampedModel):
    question = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name=_("Question"),
        help_text=_("The question being asked in the FAQ.")
    )
    answer = models.TextField(
        null=False,
        blank=False,
        verbose_name=_("Answer"),
        help_text=_("The answer to the FAQ question.")
    )
    order = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name=_("Display Order"),
        help_text=_("Controls the order FAQs are displayed.")
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name=_("Visibility"),
        help_text=_("Determines if the FAQ is visible on the site.")
    )

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
        ordering = ['order', 'question']

    def __str__(self):
        return self.question