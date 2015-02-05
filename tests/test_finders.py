# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.management import call_command

from model_mommy import mommy
from mock import patch

from cdn_js.models import CDNFile


class FakeBackend(object):

    def list_package_files(self, *args, **kwargs):
        return ['jquery.js', 'jquery.min.js', 'jquery.min.map']

    def get_file_url(self, package, version, filename):
        return ('http://cdn.jsdelivr.net/' + package + '/' + version + '/' +
                filename)


class CDNFinderTestCase(TestCase):

    @classmethod
    def setUpClass(self):
        call_command('bower', 'install')
        # create some garbage
        mommy.make(CDNFile, _quantity=3)
        with patch('cdn_js.backends.cdn_jsdelivr', FakeBackend()):
            call_command('collectstatic', interactive=False)

    def test_jquery_links_are_saved(self):
        fake_backend = FakeBackend()
        for filename in fake_backend.list_package_files():
            self.assertTrue(CDNFile.objects.filter(
                            url=fake_backend.get_file_url('jquery', '2.1.3',
                                                          filename)))

    def test_clean_up(self):
        self.assertEquals(CDNFile.objects.count(), 3)
