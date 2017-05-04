# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.hashers import make_password
from django.db import migrations


def add_admin(apps, schema_editor):
    """
    Add a default superuser: admin/admin when migrate
    """
    User = apps.get_model("auth", "User")
    User.objects.update_or_create(
        username="admin", defaults={
            "password": make_password("admin"),
            "is_superuser": True,
            "is_staff": True
        })


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(add_admin)
    ]
