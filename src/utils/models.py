import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import BaseModelQuerySet


class BaseModel(models.Model):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    objects = BaseModelQuerySet.as_manager()

    class Meta:
        abstract = True


class UUIDPkBaseModel(BaseModel):
    id = models.UUIDField(_("Primary Key"), primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
