from .compat import HTTPError


class PinboardError(Exception):
    pass

class PinboardServerError(HTTPError):
    pass

class PinboardServiceUnavailable(HTTPError):
    pass

class PinboardAuthenticationError(HTTPError):
    pass

class PinboardForbiddenError(HTTPError):
    pass

