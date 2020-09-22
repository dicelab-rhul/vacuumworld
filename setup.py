#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 21:22:31 2019

@author: ben
"""

import setuptools

setuptools.setup(name='vacuumworld',
      version='4.1.7',
      description='',
      url='https://github.com/dicelab-rhul/vacuumworld',
      author='Benedict Wilkins',
      author_email='brjw@hotmail.co.uk',
      license='GNU3',
      packages=setuptools.find_packages(),
      include_package_data=True,
      install_requires=['pystarworlds>=0.0.3', 'pillow'],
      classifiers=[
        "Programming Language :: Python :: 3.7",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
      ])
