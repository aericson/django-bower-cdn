# -*- coding: utf-8 -*-

from model_mommy import mommy

from cdn_js.models import CDNFile
from tests.utils import FakeBackend, CDNTestCase, TEST_JQUERY_VERSION


class CDNFinderTestCase(CDNTestCase):

    @classmethod
    def preCollectStatic(cls):
        # create some garbage
        mommy.make(CDNFile, _quantity=3)
        # create a wrong/old url
        CDNFile.objects.create(version=TEST_JQUERY_VERSION, url='asdada',
                               filename='jquery.js', package='jquery')

    def test_jquery_links_are_saved(self):
        fake_backend = FakeBackend()
        for filename in fake_backend.list_package_files('jquery',
                                                        TEST_JQUERY_VERSION):
            self.assertTrue(CDNFile.objects.filter(
                            url=fake_backend.get_file_url('jquery',
                                                          TEST_JQUERY_VERSION,
                                                          filename)))

    def test_clean_up(self):
        self.assertEquals(CDNFile.objects.count(), 17)
