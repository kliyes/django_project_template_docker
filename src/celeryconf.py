# -*- coding: utf-8 -*-

import os

from django.conf import settings

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

app = Celery()

CELERY_TIMEZONE = settings.TIME_ZONE

app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()
