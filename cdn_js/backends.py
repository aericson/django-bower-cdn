# -*- coding: utf-8 -*-

import requests
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


class CDNAPIJsDelivrBackend(object):

    def __init__(self, basepath, queryurl):
        self.basepath = basepath
        self.queryurl = queryurl

    def join_url(self, baseurl, *args):
        url = baseurl if baseurl.endswith('/') else baseurl + '/'
        for arg in args[:-1]:
            url = urljoin(url, arg if arg.endswith('/') else arg + '/')
        if args:
            url = urljoin(url, args[-1].rstrip('/') if args[-1].endswith('/')
                          else args[-1])
        return url

    def list_package_files(self, package_name, version):
        url = self.join_url(self.queryurl, package_name, version)
        try:
            return requests.get(url).json()
        except ValueError:
            return []

    def get_file_url(self, package_name, version, filename):
        url = self.join_url(self.basepath, package_name, version, filename)
        if requests.head(url).status_code == requests.codes.OK:
            return url
        else:
            return None


cdn_jsdelivr = CDNAPIJsDelivrBackend(
    basepath='https://cdn.jsdelivr.net/',
    queryurl='https://api.jsdelivr.com/v1/jsdelivr/libraries/')

cdn_google = CDNAPIJsDelivrBackend(
    basepath='https://ajax.googleapis.com/ajax/libs/',
    queryurl='https://api.jsdelivr.com/v1/google/libraries/')

cdn_bootstrap = CDNAPIJsDelivrBackend(
    basepath='https://maxcdn.bootstrapcdn.com',
    queryurl='https://api.jsdelivr.com/v1/bootstrap/libraries/')
