#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 13:42:09 2019

@author: ben
"""

import os,re

TODO_FILE = '../TODO.txt'
TODO_REGEX = re.compile(r'.*#.*TODO.*')

FILES = []

for d in os.walk('..'):
    FILES.extend([d[0] + '/' + f for f in d[2] if f.endswith('.py')])

FILES


with open(TODO_FILE, 'w') as g:
    for file in FILES: 
        with open(file, 'r') as f:
            for i, line in enumerate(f.readlines()):
                if re.search(TODO_REGEX, line):
                    g.write(':'.join([f.name[3:], str(i), line]))
            
        
        
