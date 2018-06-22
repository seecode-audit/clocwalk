#!/usr/bin/env python
# coding: utf-8

import os
import sys
import glob
import logging
import inspect

from clocwalk.lib.data import paths
from clocwalk.lib.data import logger
from clocwalk.lib.data import kb
from clocwalk.lib.data import conf
from clocwalk.lib.exception import SyntaxException
from clocwalk.lib.exception import GenericException


def _setPluginFunctions():
    """
    Loads plugin detecting functions from script(s)
    """
    plugins = glob.glob(os.path.join(paths.PLUGINS_PATH, "*.py"))
    if not plugins:
        plugins = glob.glob(os.path.join(paths.PLUGINS_PATH, "*.pyc"))

    for found in plugins:
        dirname, filename = os.path.split(found)
        dirname = os.path.abspath(dirname)

        if filename in ("__init__.py", "__init__.pyc"):
            continue

        if filename.endswith('.pyc'):
            pluginName = filename[:-4]
        else:
            pluginName = filename[:-3]

        logger.debug("loading plugin script '%s'" % pluginName)

        if dirname not in sys.path:
            sys.path.insert(0, dirname)

        try:
            if pluginName in sys.modules:
                del sys.modules[pluginName]
            module = __import__(pluginName)
        except ImportError as msg:
            raise SyntaxException("cannot import plugin script '%s' (%s)" % (pluginName, msg))

        _ = dict(inspect.getmembers(module))
        if "start" not in _:
            errMsg = "missing function 'start(**kwargs)' "
            errMsg += "in start script '%s'" % found
            raise GenericException(errMsg)
        else:
            kb.pluginFunctions.append((_["start"], _.get("__product__", pluginName)))


def _setConfigFile():
    """

    :return:
    """
    import yaml
    with open(paths.config_path) as fp:
        conf.cloc = yaml.load(fp)


def setVerbosity():
    """
    This function set the verbosity of output messages.
    """

    if conf.verbose is None:
        conf.verbose = 1

    conf.verbose = int(conf.verbose)

    if conf.verbose == 0:
        logger.setLevel(logging.ERROR)
    elif conf.verbose == 1:
        logger.setLevel(logging.INFO)
    elif conf.verbose >= 2:
        logger.setLevel(logging.DEBUG)


def init():
    """
    Set attributes into both configuration and knowledge base singletons
    based upon command line and configuration file options.
    """
    setVerbosity()
    _setPluginFunctions()
    _setConfigFile()
