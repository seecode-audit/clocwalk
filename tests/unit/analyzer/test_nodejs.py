#!/usr/bin/env python
# coding: utf-8

import os

from tests.common import TestCase
from tests.common import EXAMPLE_DATA_PATH

from clocwalk.plugins.nodejs import start


class NodeJSTestCase(TestCase):

    def setUp(self):
        pass

    def test_start(self):
        code_path = os.path.join(EXAMPLE_DATA_PATH, 'plugins', 'nodejs')
        result = start(code_dir=code_path)
        for item in result:
            self.assertIsNotNone(item['name'])


