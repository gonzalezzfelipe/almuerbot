#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os
import pathlib
from setuptools import setup, find_packages

setup_dir = os.path.dirname(__file__)

with open(os.path.join(setup_dir, 'almuerbot', 'VERSION'), 'r') as vf:
    version = vf.read().strip()


def parse_requirements_txt(filename='requirements.txt'):
    requirements = open(os.path.join(os.path.dirname(__file__),
                                     filename)).readlines()
    # remove whitespaces
    requirements = [line.strip().replace(' ', '') for line in requirements]
    # remove all the requirements that are comments
    requirements = [line for line in requirements if not line.startswith('#')]
    # remove empty lines
    requirements = list(filter(None, requirements))
    return requirements


setup(
    name='almuerbot',
    version=version,
    author="Felipe Gonzalez",
    author_email='gonzalezz_felipe@hotmail.com',
    install_requires=parse_requirements_txt(),
    include_package_data=True,
    data_files=[
        ('', [
            'README.rst', 'stardust/VERSION', 'CHANGELOG.rst',
            'requirements.txt', 'requirements_dev.txt'
        ]),
    ],
    packages=['almuerbot', 'almuerbot.app'],
    zip_safe=False,
)
