We often want to render different HTML templates for phones, tablets, and desktop browsers. Or for AB testing. ``django-variatmpl``  make it easy. By setting ``request.variant``, you can render the template according to that ``request.variant``. This library is heavily inspired by `Action Pack Variants <http://guides.rubyonrails.org/4_1_release_notes.html#action-pack-variants>`_.


|travis| |coveralls| |version| |license|

Quick start
=============

1. Install ``django-variantmpl``

.. code-block:: bash

 $ pip install django-variantmpl

2. Change ``django.shortcuts.render`` to ``variantmpl.shortcuts.render`` in your views.

* And set ``request.variant`` property.

.. code-block:: python

 # views.py --

 # from django.shortcuts import render
 from variantmpl.shortcuts import render # <- add

 def sample(request):

     # Set variant value
     request.variant = 'v2'

     return render(request, 'index.html')

3. Prepare variant templates.

.. code-block:: bash

 $ echo 'sample v1' > templates/index.html
 $ echo 'sample v2' > templates/index+v2.html

4. Confirm ``views.sample`` display in  your browser.

* You can see **sample v2**. 
* It is the result of loading the template(``index+v2.html``) based on ``request.variant``.

Features
=========

render
--------

Use instead of ``django.shortcuts.render``.

.. code-block:: python

 # views.py --

 from variantmpl.shortcuts import render

 def sample(request):
     request.variant = 'v2'

     # Actually "index+v2.html" is rendered
     return render(request, 'index.html')


render_to_response
--------------------

Use instead of ``django.shortcuts.render_to_response``.

.. code-block:: python

 # views.py --

 from variantmpl.shortcuts import render_to_response

 def sample(request):

     # Actually "index+v2.html" is rendered
     return render_to_response(request, 'index.html', variant='v2')

You can set ``variant`` as a keyword argument.

render_to_string
--------------------

Use instead of ``django.template.loader.render_to_string``.

.. code-block:: python

 # views.py --

 from django.http import HttpResponse

 from variantmpl.template.loader import render_to_string

 def sample(request):
     request.variant = 'v2'

     # Actually "index+v2.html" is rendered
     content = render_to_string('index.html', request=request)
     return HttpResponse(content)


TemplateResponse
--------------------

Use instead of ``django.template.response.TemplateResponse``.

.. code-block:: python

 # views.py --

 from django.views.generic import TemplateView
 from variantmpl.template.response import TemplateResponse

 class SampleView(TemplateView):
     template_name = 'sample/index.html'
     response_class = TemplateResponse # Replace response class

     def get(self, request, **kwargs):
         request.variant = 'v2'

         # Actually "index+v2.html" is rendered
         return super().get(request, **kwargs)

 sample = SampleView.as_view()

Monkey patching Django's functions/classes
-----------------------------------------------

It is difficult to rewrite all code with large codes already to ``variantmpl`` code. In such a case, you can apply Monkey patch to Django's functions/classes.

**Caution** : This feature is experimental. This may be deleted in the future if unexpected bad effects occur.

.. code-block:: python

 # settings.py --

 SECRET_KEY = 'xxxxxx'

 # You must write this code below SECRET_KEY.
 from variantmpl import monkey
 monkey.patch_all()

.. code-block:: python

 # views.py --

 # You don't need to replace to 'variantmpl'.
 from django.shortcuts import render

 def sample(request):
     request.variant = 'v2'

     # Actually "index+v2.html" is rendered
     return render(request, 'index.html')

All targets for monkey patching.

.. code-block::

 django.shortcuts.render
 django.shortcuts.render_to_response
 django.template.loader.render_to_string
 django.template.response.TemplateResponse.resolve_template

 They are replaced by the functions/methods of the same name in `variantmpl`.


Configuration
===============

VARIANTMPL_VARIANT_FORMAT
-----------------------------------

You can change ``variant`` format. default: ``+variant``.

.. code-block:: python

 # settings.py --
 VARIANTMPL_VARIANT_FORMAT = '@{variant}'

::

 # The lookup target template name changes as follows.

 "index+variant.html" -> "index@variant.html"


VARIANTMPL_PROPERTY_NAME
-----------------------------------

You can rename ``request.variant`` property.

.. code-block:: python

 # settings.py --
 VARIANTMPL_PROPERTY_NAME = 'mutation'

.. code-block:: python

 # You can set 'mutation' instead of 'varaiant'
 request.mutation = 'v2'


VARIANTMPL_TEMPLATE_FORMAT
-----------------------------------

You can change the position of the variant inserted into template path.

.. code-block:: python

 # For example, you have this path.
 render('sample1/sample2/index.html')

 # variantmpl inserts the variant(v2) as follows.
 'sample1/sample2/index+v2.html'

 # At this time, VARIANTMPL_TEMPLATE_FORMAT is like this. (default)
 VARIANTMPL_TEMPLATE_FORMAT = '{dirpath}{filename}{variant}.{ext}'
 dirpath  # => 'sample1/sample2/'
 filename # => 'index'
 variant  # => '+v2'
 ext      # => 'html'

Change this format like this.

.. code-block:: python

 VARIANTMPL_TEMPLATE_FORMAT = '{variant}/{dirpath}{filename}.{ext}'

 # variantmpl inserts the variant(v2) as follows.
 '+v2/sample1/sample2/index.html'

In this case templates layout will change as follows

::

 templates
   ├── +v2
   │   └── sample1
   │       └── sample2
   │           └── index.html
   └── sample1
       └── sample2
           └── index.html


Python and Django Support
=========================

* Python 3.4 later
* Django 1.10 later
* Support only the latest 3 versions.

License
=======

MIT Licence. See the LICENSE file for specific terms.

History
=======

0.1.0(12 26, 2017)
---------------------
* First release

.. |travis| image:: https://travis-ci.org/tell-k/django-variantmpl.svg?branch=master
    :target: https://travis-ci.org/tell-k/django-variantmpl

.. |coveralls| image:: https://coveralls.io/repos/tell-k/django-variantmpl/badge.png
    :target: https://coveralls.io/r/tell-k/django-variantmpl
    :alt: coveralls.io

.. |version| image:: https://img.shields.io/pypi/v/django-variantmpl.svg
    :target: http://pypi.python.org/pypi/django-variantmpl/
    :alt: latest version

.. |license| image:: https://img.shields.io/pypi/l/django-variantmpl.svg
    :target: http://pypi.python.org/pypi/django-variantmpl/
    :alt: license
