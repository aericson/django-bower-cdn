#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import cdn_js

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = cdn_js.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-bower-cdn',
    version=version,
    description="""Automatic add CDN for your local django-bower installed javascript libs""",
    long_description=readme + '\n\n' + history,
    author='André Ericson',
    author_email='de.ericson@gmail.com',
    url='https://github.com/aericson/django-bower-cdn',
    packages=[
        'cdn_js',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="MIT",
    zip_safe=False,
    keywords='django-bower-cdn',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
