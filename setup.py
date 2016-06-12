#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re

from setuptools import setup, find_packages
# noinspection PyPep8Naming
from setuptools.command.test import test as TestCommand

#
#
#

here = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    # noinspection PyAttributeOutsideInit
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


def find_version(*file_path):
    path = os.path.join(here, *file_path)

    with open(path) as f:
        version_file = f.read()

    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)

    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")

#
#
#

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

with open('requirements.txt') as requirements_file:
    requirements = [line for line in requirements_file if not line.startswith('pytest')]

test_requirements = [
    'pytest'
]

#
#
#

setup(
    name='confulaga',
    version=find_version('confulaga', '__init__.py'),
    description="Python library for parsing custom configuration file.",
    long_description=readme + '\n\n' + history,
    author="Irsyad Asyhari Lubis",
    author_email='irsyad.lubis@gmail.net',
    url='',
    packages=find_packages(),
    package_dir={'confulaga':
                     'confulaga'},
    include_package_data=True,
    install_requires=requirements,
    license="Proprietary",
    zip_safe=False,
    keywords='vres',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
    extras_require={
        'testing': ['pytest']
    }
)
