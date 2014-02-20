#!/usr/bin/env python
# Copyright (C) 2014 by Brian Neal.
# This file is part of purple, the PURPLE (Cipher Machine 97) simulation.
# purple is released under the MIT License (see LICENSE.txt).

from distutils.core import setup
from os.path import join, dirname

import purple

setup(
    name='purple',
    version=purple.__version__,
    author='Brian Neal',
    author_email='bgneal@gmail.com',
    url='https://bitbucket.org/bgneal/purple/',
    license='MIT',
    description='Simulation of the WW2 Japanese PURPLE cipher machine.',
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    packages=['purple', 'purple.tests'],
    scripts=['scripts/purple'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Communications',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
