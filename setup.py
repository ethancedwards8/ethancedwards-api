#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Ethan Edwards"

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    README = readme_file.read()

setup(
    name='ethancedwards_api',
    version='0.1',
    py_modules=['ethancedwards_api'],
    entry_points={
        'console_scripts': ['ethancedwards_api = ethancedwards_api:run']
    },
)
