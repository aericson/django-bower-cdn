import responses
from unittest import TestCase
from cdn_js.backends import cdn_jsdelivr


class TestCDNJSDelivrBackend(TestCase):

    @responses.activate
    def test_list_package_files(self):
        responses.add(responses.GET,
                      'http://api.jsdelivr.com/v1/jsdelivr/libraries/jquery/2.1.3',
                      body='["jquery.js", "jquery.min.js", "jquery.min.map"]')
        responses.add(responses.GET,
                      'http://api.jsdelivr.com/v1/jsdelivr/libraries/nonexistentpackage/2.3.3',
                      status=500)
        self.assertEquals(cdn_jsdelivr.list_package_files('jquery', '2.1.3'),
                          ['jquery.js', 'jquery.min.js', 'jquery.min.map'])
        self.assertEquals(cdn_jsdelivr.list_package_files('nonexistentpackage',
                                                          '2.3.3'), None)

    @responses.activate
    def test_get_file_url(self):
        responses.add(responses.HEAD,
                      'http://cdn.jsdelivr.net/jquery/2.1.3/jquery.js')
        responses.add(responses.HEAD,
                      'http://cdn.jsdelivr.net/jquasdery/2.1.3/jquery.js',
                      status=404)
        self.assertEquals(cdn_jsdelivr.get_file_url('jquery', '2.1.3',
                                                    'jquery.js'),
                          'http://cdn.jsdelivr.net/jquery/2.1.3/jquery.js')
        self.assertEquals(cdn_jsdelivr.get_file_url('jquasdery', '2.1.3',

                                                    'jquery.js'), None)
