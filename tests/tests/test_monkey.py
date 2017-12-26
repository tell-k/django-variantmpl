from django.test import TestCase
from django.test.client import RequestFactory


class TestPatchAll(TestCase):

    def _callFUT(self):
        from variantmpl.monkey import patch_all
        return patch_all()

    def tearDown(self):
        from variantmpl.monkey import unpatch_all
        unpatch_all()

    def test_patch_all(self):
        self._callFUT()

        from variantmpl.conf import settings
        from django.shortcuts import render
        from django.shortcuts import render_to_response
        from django.template.loader import render_to_string
        from django.template.response import TemplateResponse

        req = RequestFactory().get('/')
        setattr(req, settings.PROPERTY_NAME, 'v2')

        with self.subTest('patch render'):
            res = render(req, 'index.html')
            self.assertEqual(res.content.strip(), b'index+v2.html')

        with self.subTest('patch render_to_response'):
            res = render_to_response('index.html', variant='v2')
            self.assertEqual(res.content.strip(), b'index+v2.html')

        with self.subTest('patch render_to_string'):
            res = render_to_string('index.html', request=req)
            self.assertEqual(res.strip(), 'index+v2.html')

        with self.subTest('patch TemplateResponse'):
            res = TemplateResponse(req, 'index.html')
            self.assertEqual(res.rendered_content.strip(), 'index+v2.html')
