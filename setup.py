# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='plmn',
    version='1.0.0',
    description='Perform Regression tests of 3G/4G Registration and Connections.',
    long_description=readme,
    author='Harsh Murari',
    author_email='harsh@rhoynar.com',
    url='https://github.com/Rhoynar/plmn-regression',
    license=license,
    packages=['plmn'],
    test_suite='tests'
)

