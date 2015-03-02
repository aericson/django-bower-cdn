# -*- coding: utf-8 -*-

from model_mommy import mommy

from cdn_js.models import CDNFile
from cdn_js.finders import CDNFinder
from tests.utils import FakeBackend, CDNTestCase, TEST_JQUERY_VERSION


class CDNFinderTest(CDNTestCase):

    @classmethod
    def setUpClass(cls):
        # if we had a version different from the one installed by bower
        CDNFile.objects.create(version="5.0", url='asdada',
                               filename='jquery.js', package='jquery')
        super(CDNFinderTest, cls).setUpClass()

    @classmethod
    def preCollectStatic(cls):
        # create some garbage
        mommy.make(CDNFile, _quantity=3)
        # create a wrong/old url
        CDNFile.objects.create(version=TEST_JQUERY_VERSION, url='asdada',
                               filename='jquery.js', package='jquery')

    def setUp(self):
        class RemovedInitFromFinder(CDNFinder):
            def __init__(self, *args, **kwargs):
                pass
        self.finder = RemovedInitFromFinder()

    def test_jquery_links_are_saved(self):
        fake_backend = FakeBackend()
        for filename in fake_backend.list_package_files('jquery',
                                                        TEST_JQUERY_VERSION):
            self.assertTrue(CDNFile.objects.filter(
                            url=fake_backend.get_file_url('jquery',
                                                          TEST_JQUERY_VERSION,
                                                          filename)))

    def test_version_not_in_bower_was_deleted(self):
        self.assertFalse(CDNFile.objects.filter(package='jquery',
                                                version='5.0').exists())

    def test_clean_up(self):
        self.assertEquals(CDNFile.objects.count(), 17)

    def test_normalize_filename(self):
        finder = self.finder
        self.assertEquals(finder.normalize_filename('/css/bootstrap.js'),
                          'bootstrap.js')
        self.assertEquals(finder.normalize_filename('css/bootstrap.js'),
                          'bootstrap.js')
        self.assertEquals(finder.normalize_filename('/css/bootstrap.js/'),
                          'bootstrap.js')
        self.assertEquals(finder.normalize_filename('css/bootstrap.js'),
                          'bootstrap.js')

    def test_normalize_filename_in_urls_dict(self):
        d = {'css/bootstrap.js': 'http://url'}
        self.finder.normalize_filename_in_urls_dict(d)
        self.assertEqual(len(d), 1)
        self.assertEqual(d['bootstrap.js'], 'http://url')

    def test_remove_duplicated_files(self):
        d = {'css/bootstrap.js': 'http://1',
             'js/bootstrap.js': 'http://2',
             'bootstrap.css': 'http://3'}
        self.finder.remove_duplicated_files(d)
        self.assertEqual(d, {'bootstrap.css': 'http://3'})
