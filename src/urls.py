"""{{ project_name }} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/{{ docs_version }}/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

Use Django Translation and Internationalization features, see:
    https://docs.djangoproject.com/en/1.11/topics/i18n/translation/#how-django-discovers-language-preference
    https://docs.djangoproject.com/en/1.11/topics/i18n/translation/#language-prefix-in-url-patterns
Examples:
prefix_default_language == True
    http://example.com/en/admin/, will display English admin site
    http://example.com/zh-hans/admin/, will display Chinese admin site
prefix_default_language == False and settings.LANGUAGE_CODE == "en":
    http://example.com/admin/, will display English admin site
    http://example.com/en/admin/, will raise 404
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin


admin.site.site_title = getattr(settings, "ADMIN_SITE_TITLE", admin.site.site_title)
admin.site.site_header = getattr(settings, "ADMIN_SITE_HEADER", admin.site.site_header)
admin.site.index_title = getattr(settings, "ADMIN_INDEX_TITLE", admin.site.index_title)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
