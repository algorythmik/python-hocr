#
# Copyright 2017 Vic.ai - Rune Loyning
#
# https://github.com/Vic-ai/python-hocr
#

from setuptools import find_packages
from distutils.core import setup
from pkgutil import get_importer

meta = get_importer('pyhocr').find_module('__init__').load_module('__init__')
__version__ = '1.0.0'

setup(
    name="pyhocr",
    version=__version__,
    description=meta.__description__,
    author='Vic.ai',
    author_email='rune@vic.ai',
    url='http://github.com/loyning/python-24so/',
    keywords='hocr',
    classifiers=[],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'beautifulsoup4',
        'six',
        'lxml'
    ],
)
