#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 21:22:31 2019

@author: ben
"""

import setuptools

from vacuumworld.common import version, author, author_email, classifiers, license, url, name, dependencies, description

setuptools.setup(
      name=name,
      version=version,
      description=description,
      url=url,
      author=author,
      author_email=author_email,
      license=license,
      packages=setuptools.find_packages(),
      include_package_data=True,
      install_requires=dependencies,
      classifiers=classifiers
)