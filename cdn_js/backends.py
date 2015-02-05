
import requests
from urlparse import urljoin


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
            return None

    def get_file_url(self, package_name, version, filename):
        return self.join_url(self.basepath, package_name, version, filename)


cdn_jsdelivr = CDNAPIJsDelivrBackend(
    basepath='http://cdn.jsdelivr.net/',
    queryurl='http://api.jsdelivr.com/v1/jsdelivr/libraries/')
