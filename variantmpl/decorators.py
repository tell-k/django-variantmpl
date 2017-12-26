"""
    variantmpl.decorators
    ~~~~~~~~~~~~~~~~~~~~~

    :author: tell-k <ffk2005 at gmail.com>
    :copyright: tell-k. All Rights Reserved.
"""
from functools import wraps

from variantmpl import get_templates, has_variant, get_variant


def wrap_render(f):
    """ decorator for django.shortcuts.render """

    @wraps(f)
    def wrapper(request, template_name, *args, **kwargs):
        if has_variant(request):
            template_name = get_templates(template_name, get_variant(request))
        return f(request, template_name, *args, **kwargs)
    return wrapper


def wrap_render_to_response(f):
    """ decorator for django.shortcuts.render_to_response """

    @wraps(f)
    def wrapper(template_name, *args, **kwargs):
        variant = kwargs.pop('variant', None)
        if variant is not None:
            template_name = get_templates(template_name, variant)
        return f(template_name, *args, **kwargs)
    return wrapper


def wrap_render_to_string(f):
    """ decorator for django.template.loader.render_to_string """

    @wraps(f)
    def wrapper(template_name, context=None, request=None, *args, **kwargs):
        if request is not None and has_variant(request):
            template_name = get_templates(template_name, get_variant(request))
        return f(template_name, context, request, *args, **kwargs)
    return wrapper


def wrap_resolve_template(f):
    """ decorator for
    django.template.response.TemplateResponse.resolve_template
    """

    @wraps(f)
    def wrapper(self, template):
        if hasattr(self, '_request') and has_variant(self._request):
            template = get_templates(template, get_variant(self._request))
        return f(self, template)
    return wrapper
