#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 13:42:09 2019

@author: ben
"""

import os,re,argparse

TODO_FILE = 'TODO.txt'
TODO_REGEX = re.compile(r'.*#.*TODO.*')

FILES = []

parser = argparse.ArgumentParser()
parser.add_argument("d")
args = parser.parse_args()

for d in  os.walk(args.d):
    FILES.extend([os.path.join(d[0], f) for f in d[2] if f.endswith('.py')])

print(FILES)

with open(TODO_FILE, 'w') as g:
    for file in FILES: 
        with open(file, 'r') as f:
            for i, line in enumerate(f.readlines()):
                line = line.strip() + '\n'
                if re.search(TODO_REGEX, line):
                    g.write(':'.join([f.name, str(i), ' ' + line]))
            
        
        
