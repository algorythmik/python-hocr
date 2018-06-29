from setuptools import find_packages
from distutils.core import setup

__version__ = '1.1.1'

setup(
    name='pyhocr',
    version=__version__,
    description='Minimalistic library for parsing and navigating the hOCR',
    author='Mojtaba',
    author_email='smt.moji@gmail.com',
    url='https://github.com/algorythmik/python-hocr/',
    keywords='hocr parse',
    classifiers=[],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'beautifulsoup4',
        'six',
        'lxml'
    ],
)
