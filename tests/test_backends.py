from unittest import TestCase
from cdn_js.backends import cdn_jsdelivr


# TODO: mock requests with responses
class TestCDNJSDelivrBackend(TestCase):

    def test_list_package_files(self):
        self.assertEquals(cdn_jsdelivr.list_package_files('jquery', '2.1.3'),
                          ['jquery.js', 'jquery.min.js', 'jquery.min.map'])
        self.assertEquals(cdn_jsdelivr.list_package_files('nonexistentpackage',
                                                          '2.3.3'), None)

    def test_get_file_url(self):
        self.assertEquals(cdn_jsdelivr.get_file_url('jquery', '2.1.3',
                                                    'jquery.js'),
                          'http://cdn.jsdelivr.net/jquery/2.1.3/jquery.js')
