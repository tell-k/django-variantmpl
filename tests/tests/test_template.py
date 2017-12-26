from django.test import TestCase
from django.test.client import RequestFactory


class TestRenderToString(TestCase):

    def _callFUT(self, template_name, context=None, request=None, using=None):
        from variantmpl.template.loader import render_to_string
        return render_to_string(template_name, context, request, using)

    def test_missing_request(self):
        content = self._callFUT('index.html', request=None)
        self.assertEqual(content.strip(), 'index.html')

    def test_missing_variant(self):
        req = RequestFactory().get('/')
        content = self._callFUT('index.html', request=req)
        self.assertEqual(content.strip(), 'index.html')

    def test_get_variant_template(self):
        from variantmpl.conf import settings

        req = RequestFactory().get('/')
        setattr(req, settings.PROPERTY_NAME, 'v2')

        content = self._callFUT('index.html', request=req)
        self.assertEqual(content.strip(), 'index+v2.html')

    def test_fallback_template(self):
        from variantmpl.conf import settings

        req = RequestFactory().get('/')
        setattr(req, settings.PROPERTY_NAME, 'v2')

        # When missing 'index2+v2.html', fallback to 'index2.html'
        content = self._callFUT('index2.html', request=req)
        self.assertEqual(content.strip(), 'index2.html')


class TestTemplateResponse(TestCase):

    def _getTargetClass(self):
        from variantmpl.template.response import TemplateResponse
        return TemplateResponse

    def _makeOne(self, request, template, context=None,
                 content_type=None, status=None, charset=None, using=None):

        return self._getTargetClass()(request, template, context,
                                      content_type, status, charset, using)

    def test_missing_variant(self):
        req = RequestFactory().get('/')
        res = self._makeOne(req, 'index.html')
        self.assertEqual(res.rendered_content.strip(), 'index.html')

    def test_get_variant_template(self):
        from variantmpl.conf import settings

        req = RequestFactory().get('/')
        setattr(req, settings.PROPERTY_NAME, 'v2')

        res = self._makeOne(req, 'index.html')
        self.assertEqual(res.rendered_content.strip(), 'index+v2.html')

    def test_fallback_template(self):
        from variantmpl.conf import settings

        req = RequestFactory().get('/')
        setattr(req, settings.PROPERTY_NAME, 'v2')

        # When missing 'index2+v2.html', fallback to 'index2.html'
        res = self._makeOne(req, 'index2.html')
        self.assertEqual(res.rendered_content.strip(), 'index2.html')
