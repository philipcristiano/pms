#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='pms',
    version='0.1.0',
    description='An application monitoring service',
    keywords = 'monitoring',
    url='https://github.com/philipcristiano/pms',
    author='Philip Cristiano',
    author_email='pms@philipcristiano.com',
    license='BSD',
    packages=['pms'],
    install_requires=[
        'configobj==4.6.0',
        'flask',
        'gevent',
        'gunicorn',
        'pymongo',
    ],
    test_suite='tests',
    long_description=read('README.rst'),
    zip_safe=True,
    entry_points="""
    [console_scripts]
    """
)
