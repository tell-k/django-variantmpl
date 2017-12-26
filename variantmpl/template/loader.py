"""
    variantmpl.template.response
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: tell-k <ffk2005 at gmail.com>
    :copyright: tell-k. All Rights Reserved.
"""

from django.template.loader import render_to_string as _render_to_string

from variantmpl import decorators


render_to_string = decorators.wrap_render_to_string(_render_to_string)
