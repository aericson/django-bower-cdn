# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.templatetags.static import StaticNode
from django.contrib.staticfiles.storage import staticfiles_storage

from cdn_js.models import CDNFile


register = template.Library()


def static(path):
    return staticfiles_storage.url(path)


class CDNStaticNode(StaticNode):

    def url(self, context):
        path = self.path.resolve(context)
        if settings.DEBUG and not getattr(settings, 'CDN_FORCE_CDN', False):
            return static(path)
        else:
            splitted = [x for x in path.split('/') if x]
            package = splitted[0]
            filename = splitted[-1]
            try:
                return CDNFile.objects.get(package=package,
                                           filename=filename).url
            # fall back to regular static lookup
            except:
                return static(path)


@register.tag('cdn_static')
def do_static(parser, token):
    """
    A template tag that returns the CDN
    path to a file in production or using
    'staticfiles' storage backend when DEBUG
    for CDN to work path must start with the
    package name.

    Usage::

        {% cdn_static path [as varname] %}

    Examples::

        {% cdn_static 'jquery/dist/jquery.js' %}
        {% cdn_static variable_with_path %}
        {% cdn_static 'jquery/dist/jquery.js' as admin_base_css %}
        {% cdn_static variable_with_path as varname %}

    """
    return CDNStaticNode.handle_token(parser, token)
