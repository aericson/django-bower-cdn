# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.management import call_command

from cdn_js.models import CDNFile
from tests.utils import CDNStaticTestAssertionsMixin, ClearCacheOfFinderMixin
from tests.utils import TEST_JQUERY_VERSION, TEST_BOOTSTRAP_VERSION


class EndToEndTest(ClearCacheOfFinderMixin, CDNStaticTestAssertionsMixin,
                   TestCase):

    @classmethod
    def setUpClass(cls):
        call_command('bower', 'install')
        call_command('collectstatic', interactive=False)

    def test_jquery(self):
        self.assertCDNStaticEqual('jquery/dist/jquery.js',
                                  'https://cdn.jsdelivr.net/jquery/' +
                                  TEST_JQUERY_VERSION + '/jquery.js')

    def test_bootstrap(self):
        self.assertCDNStaticEqual('bootstrap/dist/css/bootstrap.css',
                                  'https://cdn.jsdelivr.net/bootstrap/' +
                                  TEST_BOOTSTRAP_VERSION +
                                  '/css/bootstrap.css')

    def test_unkown(self):
        self.assertCDNStaticEqual('jquery/src/ajax.js',
                                  '/static/jquery/src/ajax.js')

    @classmethod
    def tearDownClass(cls):
        CDNFile.objects.all().delete()
        super(EndToEndTest, cls).tearDownClass()
