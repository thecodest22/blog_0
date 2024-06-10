from django.conf import settings

from django_minify_html.middleware import MinifyHtmlMiddleware


class ProjectMinifyHtmlMiddleware(MinifyHtmlMiddleware):
    if settings.DEBUG:
        minify_args = MinifyHtmlMiddleware.minify_args | {
            'keep_comments': True,
        }
