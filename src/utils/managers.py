# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class BaseManager(models.Manager):

    def get_by(self, first=True, *args, **kwargs):
        """
        Better get objects, return None or object

        :param first: return the first object match query or raise MultipleObjectsReturned exception
        :param args: query args
        :param kwargs: query kwargs
        :return: object or None
        """
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None
        except self.model.MultipleObjectsReturned as e:
            if first:
                return self.filter(*args, **kwargs).first()
            raise e

    def get_by_id(self, _id):
        """
        Shortcut of self.get_by(id=_id)

        :param _id: object id to query
        :return: object or None
        """
        return self.get_by(id=_id)
