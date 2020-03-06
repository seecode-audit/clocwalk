#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import

import os
import unittest

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLE_DATA_PATH = os.path.join(BASEDIR, 'tests', 'example_data')

from clocwalk.libs.core.common import banner
from clocwalk.libs.core.option import init
from clocwalk.libs.core.option import setConfigFile


class TestCase(unittest.TestCase):

    def setUp(self):
        init()
        setConfigFile()

    def tearDown(self):
        pass
