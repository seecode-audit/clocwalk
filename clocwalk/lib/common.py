#!/usr/bin/env python
# coding: utf-8

import os
import re
import sys

from clocwalk.lib.data import paths
from clocwalk.lib.log import LOGGER_HANDLER
from clocwalk.lib.settings import BANNER


def banner():
    _ = BANNER
    if not getattr(LOGGER_HANDLER, "is_tty", False):
        _ = re.sub("\033.+?m", "", _)
    print(_)


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
