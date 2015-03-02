# -*- coding: utf-8 -*-

from django.template import Template, Context

from tests.utils import CDNTestCase, TEST_JQUERY_VERSION


class CDNStaticTestCase(CDNTestCase):

    def assertCDNStaticEqual(self, content, expected):
        t = Template("{%% load cdn %%}{%% cdn_static '%s' %%}" % content)
        self.assertEquals(expected, t.render(Context({})))

    def test_cdn_js_with_debug_unknown_file(self):
        with self.settings(DEBUG=True):
            self.assertCDNStaticEqual('js/hello.js', '/static/js/hello.js')

    def test_cdn_js_with_debug_known_file(self):
        with self.settings(DEBUG=True):
            self.assertCDNStaticEqual('jquery/dist/jquery.js',
                                      '/static/jquery/dist/jquery.js')

    def test_cdn_js_without_debug_known_file(self):
        self.assertCDNStaticEqual('jquery/dist/jquery.js',
                                  'https://cdn.jsdelivr.net/%s/%s/%s' %
                                  ('jquery', TEST_JQUERY_VERSION, 'jquery.js'))

    def test_cdn_js_without_debug_unknown_file(self):
        self.assertCDNStaticEqual('jquery/src/ajax.js',
                                  '/static/jquery/src/ajax.js')