# -*- coding: utf-8 -*-

from tests.utils import (CDNTestCase, TEST_JQUERY_VERSION,
                         CDNStaticTestAssertionsMixin, TEST_BOOTSTRAP_VERSION)


class CDNStaticTest(CDNStaticTestAssertionsMixin, CDNTestCase):

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

    def test_cdn_css_without_debug_from_bootstrap(self):
        self.assertCDNStaticEqual('bootstrap/dist/css/bootstrap.css',
                                  'https://cdn.jsdelivr.net/bootstrap/' +
                                  TEST_BOOTSTRAP_VERSION +
                                  '/css/bootstrap.css')

    def test_with_leading_slash(self):
        self.assertCDNStaticEqual('jquery/dist/jquery.js/',
                                  'https://cdn.jsdelivr.net/%s/%s/%s' %
                                  ('jquery', TEST_JQUERY_VERSION, 'jquery.js'))

    def test_with_starting_with_slash(self):
        self.assertCDNStaticEqual('/jquery/dist/jquery.js',
                                  'https://cdn.jsdelivr.net/%s/%s/%s' %
                                  ('jquery', TEST_JQUERY_VERSION, 'jquery.js'))
