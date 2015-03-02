# -*- coding: utf-8 -*-

import responses
from unittest import TestCase
from cdn_js.backends import cdn_jsdelivr

from tests.utils import TEST_JQUERY_VERSION


class CDNJSDelivrBackendTest(TestCase):

    @responses.activate
    def test_list_package_files(self):
        responses.add(responses.GET,
                      'http://api.jsdelivr.com/v1/jsdelivr/libraries/jquery/' +
                      TEST_JQUERY_VERSION,
                      body='["jquery.js", "jquery.min.js", "jquery.min.map"]')
        responses.add(responses.GET,
                      'http://api.jsdelivr.com/v1/jsdelivr/libraries/'
                      'nonexistentpackage/2.3.3',
                      status=500)
        self.assertEquals(cdn_jsdelivr.list_package_files('jquery',
                          TEST_JQUERY_VERSION),
                          ['jquery.js', 'jquery.min.js', 'jquery.min.map'])
        self.assertEquals(cdn_jsdelivr.list_package_files('nonexistentpackage',
                                                          '2.3.3'), None)

    @responses.activate
    def test_get_file_url(self):
        responses.add(responses.HEAD,
                      'http://cdn.jsdelivr.net/jquery/%s/jquery.js' %
                      TEST_JQUERY_VERSION)
        responses.add(responses.HEAD,
                      'http://cdn.jsdelivr.net/jquasdery/%s/jquery.js' %
                      TEST_JQUERY_VERSION,
                      status=404)
        self.assertEquals(cdn_jsdelivr.get_file_url('jquery',
                                                    TEST_JQUERY_VERSION,
                                                    'jquery.js'),
                          'http://cdn.jsdelivr.net/jquery/%s/jquery.js'
                          % TEST_JQUERY_VERSION)
        self.assertEquals(cdn_jsdelivr.get_file_url('jquasdery',
                                                    TEST_JQUERY_VERSION,
                                                    'jquery.js'), None)
