#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This software is distributed under the two-clause BSD license.

import codecs
import os
import re

from setuptools import setup

root_dir = os.path.abspath(os.path.dirname(__file__))


def get_version(package_name):
    version_re = re.compile(r"^__version__ = [\"']([\w_.-]+)[\"']$")
    package_components = package_name.split('.')
    init_path = os.path.join(root_dir, *(package_components + ['__init__.py']))
    with codecs.open(init_path, 'r', 'utf-8') as f:
        for line in f:
            match = version_re.match(line[:-1])
            if match:
                return match.groups()[0]
    return '0.1.0'


PACKAGE = 'telirc'


setup(
    name='telirc',
    version=get_version(PACKAGE),
    description="A simple IRC notifier",
    long_description=''.join(codecs.open('README.rst', 'r', 'utf-8').readlines()),
    author="Raphaël Barrois",
    author_email='raphael.barrois+telirc@polytechnique.org',
    url='https://github.com/rbarrois/telirc',
    keywords=['telirc', 'irc', 'notify', 'bot'],
    packages=['telirc'],
    scripts=['bin/telirc'],
    install_requires=[
        'bottom>=0.9.13',
    ],
    license='BSD',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Topic :: Communications",
        "Topic :: System :: Monitoring",
    ],
    test_suite='tests',
)
