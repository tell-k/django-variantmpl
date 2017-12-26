"""
    variantmpl.monkey
    ~~~~~~~~~~~~~~~~~

    :author: tell-k <ffk2005 at gmail.com>
    :copyright: tell-k. All Rights Reserved.
"""

from django import shortcuts
from django.template import loader
from django.template import response

from variantmpl.shortcuts import render_to_response, render
from variantmpl.template.loader import render_to_string
from variantmpl.template.response import TemplateResponse


_originals = {
    'render_to_response': shortcuts.render_to_response,
    'render': shortcuts.render,
    'render_to_string': loader.render_to_string,
    'resolve_template': response.TemplateResponse.resolve_template,
}


def patch_all():
    shortcuts.render_to_response = render_to_response
    shortcuts.render = render
    loader.render_to_string = render_to_string

    replaced = TemplateResponse.resolve_template
    response.TemplateResponse.resolve_template = replaced


def unpatch_all():
    shortcuts.render_to_response = _originals['render_to_response']
    shortcuts.render = _originals['render']
    loader.render_to_string = _originals['render_to_string']
    response.TemplateResponse.resolve_template = _originals['resolve_template']
