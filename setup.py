# -*- coding: utf-8 -*-
from distutils.core import setup

import setuptools

with open('./README.md') as file:
    long_desc = file.read()

setup(
    name='BestArbitrage',
    author='Vlad Kochetov',
    author_email='vladyslavdrrragonkoch@gmail.com',
    packages=setuptools.find_packages(),
    version='0.3.2',
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
    download_url='https://github.com/VladKochetov007/BestArbitrage/archive/0.3.2.tar.gz',
)
