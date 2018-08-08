"""{{ project_name }} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/{{ docs_version }}/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path


admin.site.site_title = getattr(settings, "ADMIN_SITE_TITLE", admin.site.site_title)
admin.site.site_header = getattr(settings, "ADMIN_SITE_HEADER", admin.site.site_header)
admin.site.index_title = getattr(settings, "ADMIN_INDEX_TITLE", admin.site.index_title)

urlpatterns = [
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
