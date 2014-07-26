import urllib2

class PinboardServerError(urllib2.HTTPError):
    pass

class PinboardAuthenticationError(urllib2.HTTPError):
    pass

class PinboardForbiddenError(urllib2.HTTPError):
    pass

