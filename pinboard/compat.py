import sys


PY2 = sys.version_info[0] == 2


if PY2:
    from urllib import urlencode
    from urllib2 import build_opener, HTTPError, HTTPSHandler, Request
    from urlparse import urlparse

    def iteritems(d):
        return d.iteritems()

else:
    from urllib.error import HTTPError
    from urllib.parse import urlencode, urlparse
    from urllib.request import build_opener, HTTPSHandler, Request

    def iteritems(d):
        return d.items()
