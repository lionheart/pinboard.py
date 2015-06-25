import urllib2

class PinboardError(Exception):
    pass

class PinboardServerError(urllib2.HTTPError):
    pass

class PinboardServiceUnavailable(urllib2.HTTPError):
    pass

class PinboardAuthenticationError(urllib2.HTTPError):
    pass

class PinboardForbiddenError(urllib2.HTTPError):
    pass

