# -*- coding: utf-8 -*-

from django.contrib.staticfiles.finders import BaseFinder
from django.utils.importlib import import_module
from django.conf import settings

from djangobower import bower

from cdn_js.models import CDNFile


class CDNFinder(BaseFinder):

    def get_backend(self):
        name = settings.CDN_BACKEND.split('.')[-1]
        module = import_module('.'.join(settings.CDN_BACKEND.split('.')[:-1]))
        return getattr(module, name)

    def __init__(self, apps=None, *args, **kwargs):
        self.storages = {}
        self.locations = []
        packages = []
        for package in bower.bower_adapter.freeze():
            pkg_name, version = package.split('#')
            packages.append(pkg_name)
            # delete left over from different versions
            CDNFile.objects.filter(package=pkg_name).exclude(
                version=version).delete()
            urls = self._find_in_cdn(pkg_name, version)
            for filename, url in urls.items():
                try:
                    cdn_file = CDNFile.objects.get(filename=filename,
                                                   package=pkg_name,
                                                   version=version)
                    if url != cdn_file.url:
                        cdn_file.url = url
                        cdn_file.save()
                except CDNFile.DoesNotExist:
                    CDNFile.objects.create(filename=filename, package=pkg_name,
                                           version=version, url=url)
        self._clean_up_database(exclude=packages)

    def _clean_up_database(self, exclude):
        CDNFile.objects.exclude(package__in=exclude).delete()

    def _find_in_cdn(self, package, version):
        urls = {}
        backend = self.get_backend()
        for filename in backend.list_package_files(package, version):
            url = backend.get_file_url(package, version, filename)
            if url:
                urls[filename] = url
        return urls

    def list(self, ignore_pattern):
        return iter([])
