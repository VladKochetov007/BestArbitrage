# -*- coding: utf-8 -*-
from distutils.core import setup

import setuptools

with open('../copy/README.md') as file:
    long_desc = file.read()

setup(
    name='BestArbitrage',
    author='Vlad Kochetov',
    author_email='vladyslavdrrragonkoch@gmail.com',
    packages=setuptools.find_packages(),
    version='4.1',
    description='Trading system for stocks, forex and others',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url='https://github.com/VladKochetov007/BestArbitrage',
    install_requires=[
        'selenium',
        'numpy'
    ],
    download_url='',
)
