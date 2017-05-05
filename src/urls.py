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
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin


# django translation
# https://docs.djangoproject.com/en/1.11/topics/i18n/translation/#how-django-discovers-language-preference
# https://docs.djangoproject.com/en/1.11/topics/i18n/translation/#language-prefix-in-url-patterns
# for example:
#
urlpatterns = i18n_patterns(
    url(r'^admin/', admin.site.urls),

    prefix_default_language=False
)
