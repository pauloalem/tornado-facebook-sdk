#!/usr/bin/env python
# -*- coding: utf-8

from distutils.core import setup
from facebook import __version__

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='tornado-facebook-sdk',
    version=__version__,
    license='OSI',
    description='A tornado based facebook graph api wrapper',
    author='Paulo Alem',
    author_email='biggahed@gmail.com',
    url='https://github.com/pauloalem/tornado-facebook-sdk',
    packages=['facebook'],
    long_description=long_description
)
