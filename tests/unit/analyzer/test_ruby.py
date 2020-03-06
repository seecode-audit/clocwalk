#!/usr/bin/env python
# coding: utf-8

import os

from tests.common import TestCase
from tests.common import EXAMPLE_DATA_PATH

from clocwalk.plugins.ruby import start


class RubyTestCase(TestCase):

    def setUp(self):
        pass

    def test_start(self):
        demo1_dependencys = [
            'rails',
            'sqlite3',
            'puma',
            'sass-rails',
            'uglifier',
            'coffee-rails',
            'jquery-rails',
            'turbolinks',
            'jbuilder',
            'byebug',
            'web-console',
            'listen',
            'spring',
            'spring-watcher-listen',
            'tzinfo-data',
            'rubyzip',
            'houston',
            'plist',
            'mobile_provision',
        ]

        demo2_dependencys = [
            'bundler',
            'rake',
            'claide',
            'xcodeproj',
            'gh_inspector',
            'colored',
            'rubyzip',
            'rest-client',
            'mobile_provision',
            'plist',
            'xcpretty',
        ]
        code_path = os.path.join(EXAMPLE_DATA_PATH, 'plugins', 'ruby')
        result = start(code_dir=code_path)
        self.assertEqual(len(demo1_dependencys)+len(demo2_dependencys), len(result))
        for item in result:
            if item['origin'] in 'demo1/Gemfile':
                self.assertIn(item['name'], demo1_dependencys)
            elif item['origin'] in 'demo2/Gemfile':
                self.assertIn(item['name'], demo2_dependencys)
