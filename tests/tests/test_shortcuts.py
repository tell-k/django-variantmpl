from django.test import TestCase
from django.test.client import RequestFactory


class TestRender(TestCase):

    def _callFUT(self, request, template_name,
                 context=None, content_type=None, status=None, using=None):

        from variantmpl.shortcuts import render
        return render(request, template_name,
                      context, content_type, status, using)

    def test_missing_variant(self):
        req = RequestFactory().get('/')
        res = self._callFUT(req, 'index.html')
        self.assertEqual(res.content.strip(), b'index.html')

    def test_get_variant_template(self):
        from variantmpl.conf import settings

        req = RequestFactory().get('/')
        setattr(req, settings.PROPERTY_NAME, 'v2')

        res = self._callFUT(req, 'index.html')
        self.assertEqual(res.content.strip(), b'index+v2.html')

    def test_fallback_template(self):
        from variantmpl.conf import settings

        req = RequestFactory().get('/')
        setattr(req, settings.PROPERTY_NAME, 'v2')

        # When missing 'index2+v2.html', fallback to 'index2.html'
        res = self._callFUT(req, 'index2.html')
        self.assertEqual(res.content.strip(), b'index2.html')


class TestRenderToResponse(TestCase):

    def _callFUT(self, template_name, context=None,
                 content_type=None, status=None, using=None, variant=None):

        from variantmpl.shortcuts import render_to_response
        return render_to_response(template_name, context, content_type,
                                  status, using, variant=variant)

    def test_missing_variant(self):
        res = self._callFUT('index.html')
        self.assertEqual(res.content.strip(), b'index.html')

    def test_get_variant_template(self):
        res = self._callFUT('index.html', variant='v2')
        self.assertEqual(res.content.strip(), b'index+v2.html')

    def test_fallback_template(self):
        # When missing 'index2+v2.html', fallback to 'index2.html'
        res = self._callFUT('index2.html', variant='v2')
        self.assertEqual(res.content.strip(), b'index2.html')
