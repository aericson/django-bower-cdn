# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.management import call_command

from mock import patch

TEST_JQUERY_VERSION = "2.1.3"


class FakeBackend(object):

    def list_package_files(self, package_name, version):
        if package_name == 'jquery':
            return ['jquery.js', 'jquery.min.js', 'jquery.min.map']
        elif package_name == 'bootstrap':
            return ["css/bootstrap-theme.css", "css/bootstrap-theme.css.map",
                    "css/bootstrap-theme.min.css", "css/bootstrap.css",
                    "css/bootstrap.css.map", "css/bootstrap.min.css",
                    "fonts/glyphicons-halflings-regular.eot",
                    "fonts/glyphicons-halflings-regular.svg",
                    "fonts/glyphicons-halflings-regular.ttf",
                    "fonts/glyphicons-halflings-regular.woff",
                    "fonts/glyphicons-halflings-regular.woff2",
                    "js/bootstrap.js", "js/bootstrap.min.js",
                    "js/npm.js"]
        else:
            return []

    def get_file_url(self, package, version, filename):
        return ('https://cdn.jsdelivr.net/' + package + '/' + version + '/' +
                filename)


class CDNTestCase(TestCase):

    @classmethod
    def preCollectStatic(cls):
        pass

    @classmethod
    def setUpClass(cls):
        call_command('bower', 'install')
        cls.preCollectStatic()
        with patch('cdn_js.backends.cdn_jsdelivr', FakeBackend()):
            call_command('collectstatic', interactive=False)
