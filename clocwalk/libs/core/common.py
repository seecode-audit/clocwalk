#!/usr/bin/env python
# coding: utf-8

import os
import re
import sys
import inspect
import fnmatch
import glob

from clocwalk.libs.core.log import LOGGER_HANDLER
from clocwalk.libs.core.settings import BANNER


def banner():
    _ = BANNER
    if not getattr(LOGGER_HANDLER, "is_tty", False):
        _ = re.sub("\033.+?m", "", _)
    print(_)


def modulePath():
    """
    This will get us the program's directory, even if we are frozen
    using py2exe
    """

    try:
        _ = sys.executable if weAreFrozen() else __file__
    except NameError:
        _ = inspect.getsourcefile(modulePath)

    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(_))))


def weAreFrozen():
    """
    Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located.
    Reference: http://www.py2exe.org/index.cgi/WhereAmI
    """

    return hasattr(sys, "frozen")


def recursive_search_files(search_dir, file_info):
    """

    :param search_dir: /etc/nginx
    :param file_info: *.conf
    :return:
    """
    file_list = []
    for p in glob.glob(os.path.join(search_dir, '*')):
        if fnmatch.fnmatch(p, file_info):
            file_list.append(p)
        elif os.path.isdir(p):
            file_list.extend(recursive_search_files(p, file_info))

    return file_list


def parse_int(str_value, default_value=0):
    """
    转换成int
    :param str_value:
    :param default_value:
    :return:
    """
    if str_value:
        try:
            result = int(str_value)
        except (ValueError, TypeError):
            result = default_value
    else:
        result = default_value
    return result


def parse_int_or_str(str_value):
    """
    :param str_value:
    :return:
    """
    result = None
    if str_value:
        if isinstance(str_value, int):
            result = str_value
        elif isinstance(str_value, str) or isinstance(str_value, bytes):
            if isinstance(str_value, bytes):
                result = str_value.decode("utf-8").strip()
            else:
                result = str_value.strip()
            try:
                result = int(result)
            except (ValueError, TypeError):
                pass
    return result


def parse_bool(str_value):
    """

    :param str_value:
    :return:
    """
    result = False
    if str_value:
        str_value = parse_int(str_value, str_value)
        if isinstance(str_value, bool):
            result = str_value

        if isinstance(str_value, int):
            if str_value < 1:
                result = False
            else:
                result = True

        if isinstance(str_value, bytes):
            str_value = str_value.decode("utf-8")

        if isinstance(str_value, str):
            str_value = str_value.strip()
            right_value = ['true', 'on']
            if str_value.lower().strip() in right_value:
                result = True

    return result


def strip(str_param, display_type=None):
    """

    :param str_param:
    :param display_type:
    :return:
    """
    result = str_param
    if str_param:
        if isinstance(str_param, str) or isinstance(str_param, bytes):
            result = str_param.strip()
            if display_type:
                if display_type.strip() == 'lower':
                    result = result.lower()
                elif display_type.strip() == 'upper':
                    result = result.upper()
    return result

