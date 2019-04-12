from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.conf import settings


class AdminImageWidget(AdminFileWidget):

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(
                f'<a '
                f'title="{_("Click to enlarge")}" '
                f'class="thumbnail highslide" '
                f'href="{value.url}" '
                f'onclick="return hs.expand(this)">'
                f'<img src="{value.url}">'
                f'</a>'
            )
        output.append(
            super(AdminImageWidget, self).render(name, value, attrs, renderer)
        )
        return mark_safe("".join(output))

    class Media:
        min = ".min" if not settings.DEBUG else ""
        js = (
            f"highslide/highslide-with-gallery{min}.js",
            "utils/js/highslide.config.js",
        )
        css = {
            "all": (
                "highslide/highslide.css",
            )
        }
