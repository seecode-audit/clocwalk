#!/usr/bin/env python
# coding: utf-8

import os
import pprint

from xml.etree import ElementTree

from tests.common import TestCase
from tests.common import EXAMPLE_DATA_PATH

from clocwalk.libs.core.data import kb
from clocwalk.libs.analyzer.mvn import start
from clocwalk.libs.analyzer.mvn import recursive_online


class POMTestCase(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.pom_dir = [
            'a/a1/pom.xml',
            'b/pom.xml',
            'c/c1/pom.xml',
            'c/c2/pom.xml',
            'pom.xml',
        ]

    def test_start_dir(self):
        pom_list = recursive_online(
            "https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-databind/2.9.9.3/jackson-databind-2.9.9.3.pom"
        )
        print(pom_list)
        for item in pom_list:
            pprint.pprint(item.dependencies)
        print(kb.dependencies)
        #tree = ElementTree.fromstring(xml)
        #print(type(tree))
        #result = start(code_dir=os.path.join(EXAMPLE_DATA_PATH, 'plugins', 'pom'))
        #for item in result:
        #    pass
            #self.assertIn(item['origin'], self.pom_dir)
