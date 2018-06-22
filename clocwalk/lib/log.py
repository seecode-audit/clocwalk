#!/usr/bin/env python
# coding: utf-8

import logging
import sys

LOGGER = logging.getLogger("clocwalk")

try:
    from clocwalk.lib.ansistrm import ColorizingStreamHandler
    LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
except ImportError:
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

FORMATTER = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")

LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(logging.INFO)
