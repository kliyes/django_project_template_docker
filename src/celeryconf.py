# -*- coding: utf-8 -*-

import os

from django.conf import settings

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

app = Celery(os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

CELERY_TIMEZONE = settings.TIME_ZONE

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
