"""
    variantmpl.shortcuts
    ~~~~~~~~~~~~~~~~~~~~

    :author: tell-k <ffk2005 at gmail.com>
    :copyright: tell-k. All Rights Reserved.
"""

from django.shortcuts import render_to_response as _render_to_response
from django.shortcuts import render as _render

from variantmpl import decorators

render_to_response = decorators.wrap_render_to_response(_render_to_response)

render = decorators.wrap_render(_render)
