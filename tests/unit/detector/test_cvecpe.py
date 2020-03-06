#!/usr/bin/env python
# coding: utf-8

from tests.common import TestCase
from tests.common import BASEDIR


from clocwalk.libs.detector.cvecpe import cpe_compare_version


class CPETestCase(TestCase):

    def setUp(self):
       pass

    def test_compare(self):
        self.assertTrue(cpe_compare_version(rule_version='2.9.0', rule_update='PRELEASE1', conf_version='2.9.0.pr1'))
        self.assertFalse(cpe_compare_version(rule_version='2.9.0', rule_update='PRELEASE2', conf_version='2.9.0.pr1'))
        self.assertFalse(cpe_compare_version(rule_version='2.9.0', rule_update='*', conf_version='2.9.0.pr1'))


