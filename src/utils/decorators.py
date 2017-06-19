# -*- coding: utf-8 -*-

from __future__ import unicode_literals


def field(label=None, **kwargs):
    """
    A decorator of admin callable-field
    Usage:
        class MyModelAdmin(admin.ModelAdmin):

            @field("Attr", allow_tags=True)
            def my_field(self, obj):
                return obj.attr

    :param label: value of callable.short_description
    :param kwargs: allow_tags, admin_order_field, ...
    :return: 
    """
    def inner(func):
        if label is not None:
            func.short_description = label
        [setattr(func, key, value) for key, value in kwargs.iteritems()]
        return func
    return inner
