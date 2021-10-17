# -*- coding: utf-8 -*-
from distutils.core import setup

import setuptools

with open('./README.md') as file:
    long_desc = file.read()
_version_ = '0.4.1'
setup(
    name='BestArbitrage',
    author='Vlad Kochetov',
    author_email='vladyslavdrrragonkoch@gmail.com',
    packages=setuptools.find_packages(),
    version=_version_,
    description='Arbitrage cryptocurrency smartly',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url='https://github.com/VladKochetov007/BestArbitrage',
    install_requires=[
        'selenium',
        'numpy',
        'colorama',
        'ccxt'
    ],
    download_url=f'https://github.com/VladKochetov007/BestArbitrage/archive/{_version_}.tar.gz',
)
