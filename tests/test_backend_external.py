# -*- coding: utf-8 -*-

from unittest import TestCase

import requests

from cdn_js.backends import cdn_jsdelivr, cdn_google, cdn_bootstrap

from tests.utils import TEST_JQUERY_VERSION


class CDNJSDelivrBackendTest(TestCase):

    def test_cdn_jsdelivr_list_package_files(self):
        self.assertItemsEqual(cdn_jsdelivr.list_package_files('jquery',
                              TEST_JQUERY_VERSION),
                              ['jquery.js', 'jquery.min.js', 'jquery.min.map'])
        self.assertEquals(cdn_jsdelivr.list_package_files('nonexistentpackage',
                                                          '2.3.3'), [])

    def test_cdn_jsdelivr_get_file_url(self):
        url = cdn_jsdelivr.get_file_url('jquery', TEST_JQUERY_VERSION,
                                        'jquery.js')
        self.assertEquals(url, 'https://cdn.jsdelivr.net/jquery/%s/jquery.js'
                          % TEST_JQUERY_VERSION)
        self.assertEquals(cdn_jsdelivr.get_file_url('jquasdery',
                                                    TEST_JQUERY_VERSION,
                                                    'jquery.js'), None)
        self.assertEquals(requests.head(url).status_code, 200)

    def test_cdn_google_list_package_files(self):
        self.assertItemsEqual(cdn_google.list_package_files('angularjs',
                                                            '1.3.14'),
                              ['angular.js', 'angular.min.js'])
        self.assertEquals(cdn_google.list_package_files('nonexistentpackage',
                                                        '2.3.3'), [])

    def test_cdn_google_get_file_url(self):
        url = cdn_google.get_file_url('angularjs', '1.3.14', 'angular.js')
        self.assertEquals(url,
                          'https://ajax.googleapis.com/ajax/libs/angularjs/%s/'
                          'angular.js'
                          % '1.3.14')
        self.assertEquals(cdn_google.get_file_url('jquasdery',
                                                  '1.3.14',
                                                  'jquery.js'), None)
        self.assertEquals(requests.head(url).status_code, 200)

    def test_cdn_bootstrap_list_package_files(self):
        self.assertItemsEqual(cdn_bootstrap.list_package_files('bootstrap',
                                                               '3.3.4'),
                              ["css/bootstrap-theme.css",
                               "css/bootstrap-theme.css.map",
                               "css/bootstrap-theme.min.css",
                               "css/bootstrap.css",
                               "css/bootstrap.css.map",
                               "css/bootstrap.min.css",
                               "fonts/glyphicons-halflings-regular.eot",
                               "fonts/glyphicons-halflings-regular.svg",
                               "fonts/glyphicons-halflings-regular.ttf",
                               "fonts/glyphicons-halflings-regular.woff",
                               "fonts/glyphicons-halflings-regular.woff2",
                               "js/bootstrap.js",
                               "js/bootstrap.min.js",
                               "js/npm.js"])
        self.assertEquals(cdn_bootstrap.list_package_files('nonexistentpackage',
                                                           '2.3.3'), [])

    def test_cdn_bootstrap_get_file_url(self):
        url = cdn_bootstrap.get_file_url('bootstrap', '3.3.4',
                                         'js/bootstrap.min.js')
        self.assertEquals(url,
                          'https://maxcdn.bootstrapcdn.com/bootstrap/%s/js/'
                          'bootstrap.min.js'
                          % '3.3.4')
        self.assertEquals(cdn_bootstrap.get_file_url('jquasdery',
                                                     '1.3.14',
                                                     'jquery.js'), None)
        self.assertEquals(requests.head(url).status_code, 200)
