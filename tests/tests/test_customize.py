from django.test import TestCase, override_settings
from django.test.client import RequestFactory


class TestCustomize(TestCase):

    def _callFUT(self, request, template_name,
                 context=None, content_type=None, status=None, using=None):

        from variantmpl.shortcuts import render
        return render(request, template_name,
                      context, content_type, status, using)

    @override_settings(VARIANTMPL_VARIANT_FORMAT='@{variant}')
    def test_change_variant_format(self):
        from variantmpl.conf import settings

        req = RequestFactory().get('/')
        setattr(req, settings.PROPERTY_NAME, 'v2')

        res = self._callFUT(req, 'index.html')
        self.assertEqual(res.content.strip(), b'index@v2.html')

    @override_settings(VARIANTMPL_PROPERTY_NAME='mutant')
    def test_change_variant_property_name(self):
        from variantmpl.conf import settings

        req = RequestFactory().get('/')
        setattr(req, settings.PROPERTY_NAME, 'v2')

        res = self._callFUT(req, 'index.html')
        self.assertEqual(res.content.strip(), b'index+v2.html')

    @override_settings(
        VARIANTMPL_TEMPLATE_FORMAT='{variant}/{dirpath}{filename}.{ext}'
    )
    def test_change_template_format(self):
        from variantmpl.conf import settings

        req = RequestFactory().get('/')
        setattr(req, settings.PROPERTY_NAME, 'v2')

        res = self._callFUT(req, 'dir1/dir2/index.html')
        self.assertEqual(res.content.strip(), b'+v2/dir1/dir2/index.html')
