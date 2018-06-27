#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import findpackages, setup

with open('README.rst', 'r') as f:
    README = f.read()

setup(
    name='django_user_extensions',
    version='0.2.1',
    description='Minor, important extensions to Django default users',
    long_description=README,
    author='Pablo Virgo',
    author_email='mailbox@pablovirgo.com',
    packages=findpackages()
)
