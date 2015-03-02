# -*- coding: utf-8 -*-
import django
from django.test import TestCase
from django.core.management import call_command
from django.template import Template, Context

from mock import patch

from cdn_js.models import CDNFile

TEST_JQUERY_VERSION = "2.1.3"
TEST_BOOTSTRAP_VERSION = "3.3.2"


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
                    "js/npm.js",
                    "js/hola.js",  # dupplicated file
                    "js/js/hola/hola.js"]  # dupplicated file
        else:
            return []

    def get_file_url(self, package, version, filename):
        return ('https://cdn.jsdelivr.net/' + package + '/' + version + '/' +
                filename)


class ClearCacheOfFinderMixin(object):
    @classmethod
    def tearDownClass(cls):
        from django.contrib.staticfiles.finders import get_finder
        if django.VERSION >= (1, 7):
            get_finder.cache_clear()
        else:
            from django.contrib.staticfiles.finders import _finders
            _finders.clear()
        super(ClearCacheOfFinderMixin, cls).tearDownClass()


class CDNTestCase(ClearCacheOfFinderMixin, TestCase):

    @classmethod
    def preCollectStatic(cls):
        pass

    @classmethod
    def setUpClass(cls):
        call_command('bower', 'install')
        cls.preCollectStatic()
        with patch('cdn_js.backends.cdn_jsdelivr', FakeBackend()):
            call_command('collectstatic', interactive=False)

    @classmethod
    def tearDownClass(cls):
        CDNFile.objects.all().delete()
        super(CDNTestCase, cls).tearDownClass()


class CDNStaticTestAssertionsMixin(object):
    def assertCDNStaticEqual(self, content, expected):
        t = Template("{%% load cdn %%}{%% cdn_static '%s' %%}" % content)
        self.assertEquals(expected, t.render(Context({})))
