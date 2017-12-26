"""
    variantmpl.template.response
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: tell-k <ffk2005 at gmail.com>
    :copyright: tell-k. All Rights Reserved.
"""

from django.template.response import TemplateResponse as BaseTemplateResponse

from variantmpl import decorators


class TemplateResponse(BaseTemplateResponse):
    pass


TemplateResponse.resolve_template = decorators.wrap_resolve_template(
    TemplateResponse.resolve_template
)
