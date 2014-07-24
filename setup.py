#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import os
from pinboard import metadata

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as file:
    long_description = file.read()

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
    "Topic :: Utilities",
    "License :: OSI Approved :: Apache Software License",
]

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
    # scripts=['scripts/pinboard']
)
