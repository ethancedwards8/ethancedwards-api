#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Ethan Edwards"

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    README = readme_file.read()

# setup_args = dict(
#     name="ethancedwards-quotes",
#     version="1.0",
#     description="A cool api that gives you my favorite quotes :)",
#     author="Ethan Edwards",
#     author_email="ethan@ethancedwards.com",
#     long_description=README,
#     long_description_content_type="text/markdown",
#     license="GPLv3",
#     packages=find_packages(),
#     url="https://github.com/ethancedwards8/api-quotes",
#     entry_points={
#         'console_scripts': ['ethancedwards-quotes = ethancedwards-quotes:run']
#     }
# )

# install_requires = [ "flask", "flask-restful" ]

# if __name__ == "__main__":
#     setup(**setup_args, install_requires=install_requires)

setup(
    name='ethancedwards_quotes',
    version='0.1',
    py_modules=['ethancedwards_quotes'],
    entry_points={
        'console_scripts': ['ethancedwards_quotes = ethancedwards_quotes:run']
    },
)
