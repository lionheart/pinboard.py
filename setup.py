#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2014-2017 Lionheart Software LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import os
from pinboard import metadata
from distutils.cmd import Command
import re
import codecs

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with codecs.open(os.path.join(os.path.dirname(__file__), "README.rst"), encoding="utf-8") as file:
    long_description = file.read()

    id_regex = re.compile(r"<\#([\w-]+)>")
    link_regex = re.compile(r"<(\w+)>")
    link_alternate_regex = re.compile(r"   :target: (\w+)")

    long_description = id_regex.sub(r"<https://github.com/lionheart/pinboard.py#\1>", long_description)
    long_description = link_regex.sub(r"<https://github.com/lionheart/pinboard.py/blob/master/\1>", long_description)
    long_description = link_regex.sub(r"<https://github.com/lionheart/pinboard.py/blob/master/\1>", long_description)
    long_description = link_alternate_regex.sub(r"   :target: https://github.com/lionheart/pinboard.py/blob/master/\1", long_description)

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
    "Topic :: Utilities",
    "License :: OSI Approved :: Apache Software License",
]

class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from test_pinboard import TestPinboardAPI
        suite = unittest.TestLoader().loadTestsFromTestCase(TestPinboardAPI)
        unittest.TextTestRunner(verbosity=2).run(suite)

setup(
    name='pinboard',
    version=metadata.__version__,
    url="http://github.com/lionheart/pinboard.py",
    long_description=long_description,
    description="A Python wrapper for Pinboard.in",
    classifiers=classifiers,
    keywords="pinboard",
    license=metadata.__license__,
    author=metadata.__author__,
    author_email=metadata.__email__,
    packages=['pinboard'],
    package_data={'': ['LICENSE', 'README.rst']},
    cmdclass={'test': TestCommand},
    scripts=["bin/pinboard"]
)
