#!/usr/bin/env python
# -*- coding: utf-8

from setuptools import setup

setup(
    name='tornado-facebook-sdk',
    version='0.1.0',
    license='OSI',
    description='A tornado based facebook graph api wrapper',
    author='Paulo Alem',
    author_email='biggahed@gmail.com',
    url='https://github.com/pauloalem/tornado-facebook-sdk',
    packages=['facebook'],
    long_description=open('README.rst').read(),
    install_requires=open("requirements.txt").read().split("\n"),
)
