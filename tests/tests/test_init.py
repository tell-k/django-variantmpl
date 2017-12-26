import unittest


class TestGetVarinatTemplate(unittest.TestCase):

    def _callFUT(self, template_name, variant):
        from variantmpl import get_variant_template
        return get_variant_template(template_name, variant)

    def test_flat_template(self):
        self.assertEqual(
            self._callFUT('index.html', 'v2'),
            'index+v2.html'
        )

    def test_multi_level_dirs(self):
        patterns = (
            {
                'template': 'depth1/index.html',
                'expected': 'depth1/index+v2.html'
            },
            {
                'template': 'depth1/depth2/index.html',
                'expected': 'depth1/depth2/index+v2.html'
            },
            {
                'template': 'depth1/depth2/depth3/index.html',
                'expected': 'depth1/depth2/depth3/index+v2.html'
            }
        )
        for p in patterns:
            with self.subTest(p['template']):
                actual = self._callFUT(p['template'], 'v2')
                self.assertEqual(actual, p['expected'])


class TestGetTemplates(unittest.TestCase):

    def _callFUT(self, template_name, variant):
        from variantmpl import get_templates
        return get_templates(template_name, variant)

    def test_template_name_is_string(self):
        patterns = (
            {
                'template': 'index.html',
                'expected': ['index+v2.html', 'index.html']
            },
            {
                'template': 'index+v2.html',
                'expected': ['index+v2.html']
            },
        )
        for p in patterns:
            with self.subTest(p['template']):
                actual = self._callFUT(p['template'], 'v2')
                self.assertEqual(actual, p['expected'])

    def test_template_name_is_list(self):
        patterns = (
            {
                'template': ['index.html', 'index2.html'],
                'expected': ['index+v2.html', 'index.html',
                             'index2+v2.html', 'index2.html']
            },
            {
                'template': ['index+v2.html', 'index2.html'],
                'expected': ['index+v2.html', 'index2+v2.html',
                             'index2.html']
            },
        )
        for p in patterns:
            with self.subTest(p['template']):
                actual = self._callFUT(p['template'], 'v2')
                self.assertEqual(actual, p['expected'])


class DummyRequest:
    """ dummy request class """


class TestGetVariant(unittest.TestCase):

    def _callFUT(self, request, default=None):
        from variantmpl import get_variant
        return get_variant(request, default)

    def test_get_value(self):
        from variantmpl.conf import settings

        req = DummyRequest()
        setattr(req, settings.PROPERTY_NAME, 'test')
        self.assertEqual(self._callFUT(req), 'test')

    def test_missing_property(self):
        req = DummyRequest()
        self.assertEqual(self._callFUT(req, 'missing'), 'missing')


class TestHasVariant(unittest.TestCase):

    def _callFUT(self, request):
        from variantmpl import has_variant
        return has_variant(request)

    def test_has_property(self):
        from variantmpl.conf import settings

        req = DummyRequest()
        setattr(req, settings.PROPERTY_NAME, 'test')
        self.assertTrue(self._callFUT(req))

    def test_has_not_property(self):
        req = DummyRequest()
        self.assertFalse(self._callFUT(req))

    def test_proeprty_is_empty(self):
        from variantmpl.conf import settings

        req = DummyRequest()
        setattr(req, settings.PROPERTY_NAME, '')  # set emtpy value
        self.assertFalse(self._callFUT(req))
