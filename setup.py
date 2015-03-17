#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('VERSION.txt', 'r') as v:
    version = v.read().strip()

with open('README.md', 'r') as r:
    readme = r.read()

download_url = (
    'https://github.com/jkeifer/arcpy-extensions/tarball/%s'
)


setup(
    name='arcpy-extensions',
    packages=['arcpy_extensions'],
    version=version,
    description=('A collection of helper functions and classes for the ArcGIS arcpy interface.'),
    long_description=readme,
    author='Jarrett Keifer',
    author_email='jkeifer0@gmail.com',
    url='https://github.com/jkeifer/arcpy-extensions',
    download_url=download_url % version,
    install_requires=[],
    license='MIT'
)
