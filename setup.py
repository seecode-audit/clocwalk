#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from clocwalk import __version__


setup(
    name='clocwalk',
    version=__version__,
    description='Project code and dependent component analysis tools.',
    author='MyKings',
    author_email='xsseroot@gmail.com',
    url='https://github.com/MyKings/clocwalk',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "clocwalk = clocwalk.cli:main"
        ]
    },
    install_requires=[
        'lxml',
        'requests',
        'PyYAML',
    ],
    extras_require={
        'dev': [
            'devpi>=2.1.0',
            'prospector>=0.10.1',
            ],
        'test': [
            'coverage>=3.7.1',
            'nose>=1.3.6',
            ],
        'docs': [
            'Sphinx>=1.3.1',
            ],
        'build': [
            'devpi>=2.1.0',
            ],
        },
    test_suite='nose.collector',
    zip_safe=False,
)
