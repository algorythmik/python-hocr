#
# Copyright 2017 Vic.ai - Rune Loyning
#
# https://github.com/Vic-ai/python-hocr
#

from setuptools import find_packages
from distutils.core import setup
from pkgutil import get_importer

meta = get_importer('hocr').find_module('__init__').load_module('__init__')

setup(
    name="pyhocr",
    version=meta.__version__,
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
