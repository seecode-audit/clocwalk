# coding: utf-8

from clocwalk.lib.datatype import AttribDict
from clocwalk.lib.log import LOGGER

# paths
paths = AttribDict()

# object to share within function and classes command
# line options and settings
conf = AttribDict()

# object to share within function and classes results
kb = AttribDict()
kb.pluginFunctions = []

# logger
logger = LOGGER
