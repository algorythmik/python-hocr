from setuptools import find_packages
from distutils.core import setup

__version__ = '4.0.0'

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
        'six>=1.11.0,<2.0.0',
        'beautifulsoup4>=4.6.0,<5.0.0',
        'lxml>=4.2.3,<5.0.0',
    ],
)
