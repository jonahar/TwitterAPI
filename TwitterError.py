__author__ = "geduldig"
__date__ = "November 30, 2014"
__license__ = "MIT"

import logging


class TwitterError(Exception):
    """Base class for Twitter exceptions"""
    pass


class TwitterConnectionError(TwitterError):
    """Raised when the connection needs to be re-established"""

    def __init__(self, value):
        super(Exception, self).__init__(value)
        logging.warning('%s %s' % (type(value), value))


class TwitterRequestError(TwitterError):
    """Raised when request fails"""

    def __init__(self, status_code, msg=None):
        if status_code >= 500 and msg is None:
            msg = 'Twitter internal error (you may re-try)'
        elif msg is None:
            msg = 'Twitter request failed'
        super(Exception, self).__init__(msg)
        self.msg = msg
        self.status_code = status_code

    def __str__(self):
        return '%s (%d)' % (self.args[0], self.status_code)
