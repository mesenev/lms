from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def hmr_script(path):
    script_origin = ''
    if settings.DEBUG and settings.WEBPACK_DEV_SERVER:
        script_origin = f'http://{settings.WEBPACK_DEV_SERVER}'
    else:
        path = static('js/' + path)

    return format_html(
        mark_safe('<script type="text/javascript" src="{}{}"></script>'),
        script_origin,
        path
    )
