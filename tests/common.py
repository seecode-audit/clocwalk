#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import


import os
import unittest

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLE_DATA_PATH = os.path.join(BASEDIR, 'tests', 'example_data')


class TestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
