# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import uuid

from django.db import models
from django.utils.translation import ugettext as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        abstract = True


class UUIDPkBaseModel(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
