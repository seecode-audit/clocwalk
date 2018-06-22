#!/usr/bin/env python
# coding: utf-8

import os
import re
import sys

from clocwalk.lib.data import paths
from clocwalk.lib.log import LOGGER_HANDLER
from clocwalk.lib.settings import BANNER
from clocwalk.lib.settings import UNICODE_ENCODING
from clocwalk.lib.settings import INVALID_UNICODE_CHAR_FORMAT


def banner():
    _ = BANNER
    if not getattr(LOGGER_HANDLER, "is_tty", False):
        _ = re.sub("\033.+?m", "", _)
    print _


def setPath():
    """
    Sets absolute paths for project directory
    """
    paths.PLUGINS_PATH = os.path.join(paths.ROOT_PATH, "plugins")
    paths.config_path = os.path.join(paths.ROOT_PATH, 'conf.yaml')


def weAreFrozen():
    """
    Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located.
    Reference: http://www.py2exe.org/index.cgi/WhereAmI
    """

    return hasattr(sys, "frozen")


def getUnicode(value, encoding=None):
    """
    Return the unicode representation of the supplied value:
    >>> getUnicode(u'test')
    u'test'
    >>> getUnicode('test')
    u'test'
    >>> getUnicode(1)
    u'1'
    """

    if isinstance(value, unicode):
        return value
    elif isinstance(value, basestring):
        flag = 3
        while True:
            try:
                if not flag:
                    break
                return unicode(value, encoding or UNICODE_ENCODING)
            except UnicodeDecodeError, ex:
                try:
                    return unicode(value, UNICODE_ENCODING)
                except:
                    value = value[:ex.start] + "".join(INVALID_UNICODE_CHAR_FORMAT % ord(_) for _ in value[ex.start:ex.end]) + value[ex.end:]
                    flag -= 1
        return unicode(str(value), errors="ignore")
    else:
        try:
            return unicode(value)
        except UnicodeDecodeError:
            return unicode(str(value), errors="ignore")  # encoding ignored for non-basestring instances


def unicodeencode(value, encoding=None):
    """
    Returns 8-bit string representation of the supplied unicode value

    >>> unicodeencode(u'foobar')
    'foobar'
    """

    retVal = value
    if isinstance(value, unicode):
        try:
            retVal = value.encode(encoding or UNICODE_ENCODING)
        except UnicodeEncodeError:
            retVal = value.encode(UNICODE_ENCODING, "replace")
    return retVal


def utf8encode(value):
    """
    Returns 8-bit string representation of the supplied UTF-8 value

    >>> utf8encode(u'foobar')
    'foobar'
    """

    return unicodeencode(value, "utf-8")
