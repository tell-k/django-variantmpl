"""
    variantmpl
    ~~~~~~~~~~

    :author: tell-k <ffk2005 at gmail.com>
    :copyright: tell-k. All Rights Reserved.
"""

__version__ = '0.1.0'

from .conf import settings


def get_variant_template(template_name, variant):
    paths = template_name.split(settings.SEP)
    fname = paths[-1]
    fnames = fname.split(settings.EXTSEP)

    filename = settings.EXTSEP.join(fnames[:-1])
    ext = fnames[-1]

    dirpath = settings.SEP.join(paths[:-1])
    if dirpath != '':
        dirpath = dirpath + settings.SEP

    variant_value = settings.VARIANT_FORMAT.format(variant=variant)
    return settings.TEMPLATE_FORMAT.format(
        dirpath=dirpath,
        filename=filename,
        variant=variant_value,
        extsep=settings.EXTSEP,
        ext=ext
    )


def get_templates(template_name, variant):
    result = []
    variant_value = settings.VARIANT_FORMAT.format(variant=variant)

    if not isinstance(template_name, (list, tuple)):
        template_name = [template_name]

    for tmpl in template_name:
        t = tmpl.split('/')[-1]

        if variant_value in t:
            result.append(tmpl)
            continue

        vt = get_variant_template(tmpl, variant)
        if vt not in result:
            result.append(vt)
        result.append(tmpl)
    return result


def get_variant(request, default=None):
    return getattr(request, settings.PROPERTY_NAME, default)


def has_variant(request):
    return hasattr(request, settings.PROPERTY_NAME) \
        and (get_variant(request, '') != '')
