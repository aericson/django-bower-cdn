# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.management import call_command

from model_mommy import mommy

from cdn_js.models import CDNFile


class CDNFinderTestCase(TestCase):

    @classmethod
    def setUpClass(self):
        call_command('bower', 'install')
        # create some garbage
        mommy.make(CDNFile, _quantity=3)
        call_command('collectstatic', interactive=False)

    def test_jquery_links_are_saved(self):
        self.assertTrue(
            CDNFile.objects.filter(
                url='http://cdn.jsdelivr.net/jquery/2.1.3/jquery.js').exists())
        self.assertTrue(
            CDNFile.objects.filter(
                url='http://cdn.jsdelivr.net/jquery/2.1.3/jquery.min.js').exists())
        self.assertTrue(
            CDNFile.objects.filter(
                url='http://cdn.jsdelivr.net/jquery/2.1.3/jquery.min.map').exists())

    def test_clean_up(self):
        self.assertEquals(CDNFile.objects.count(), 3)
