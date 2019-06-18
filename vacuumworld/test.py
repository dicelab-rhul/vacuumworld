#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 17:38:30 2019

@author: ben
"""

import re

m = map(int, re.findall(r'\d+', "(1,2)"))
print()

for i in m:
    print(i)