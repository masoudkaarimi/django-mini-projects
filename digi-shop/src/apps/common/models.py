import uuid

from django.db import models

from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Creation Date"),
        help_text=_("The date and time when the record was created. (Auto-generated)")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Update Date"),
        help_text=_("The date and time when the record was last updated. (Auto-generated)")
    )

    class Meta:
        abstract = True


class BaseModel(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def activate(self):
        self.is_active = True
        self.save(update_fields=['is_active'])

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def __str__(self):
        return f"{self.__class__.__name__} {self.id}"
