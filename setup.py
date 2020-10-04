#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 21:22:31 2019

@author: ben
"""

import setuptools

from common import version, author, author_email, classifiers, license, url, name, dependencies, description


setuptools.setup(
      name=name,
      version=version,
      description=description,
      url=url,
      author=author,
      author_email=author_email,
      license=license,
      packages=[p for p in setuptools.find_packages() if "legacy" not  in p],
      include_package_data=True,
      install_requires=dependencies,
      classifiers=classifiers
)