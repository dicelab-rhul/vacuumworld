#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:39:05 2019

@author: ben
"""


import os
import vwc

import re



class MalformedVWFile(Exception):
    def __init__(self, message):
        self.message = message

VALID_OPTIONS = {'auto_play': lambda x: x == 'true', 
                 'grid_size': lambda x: int(x)}

def load(file, env):
    f = open(os.curdir + file)
    env.reset(env.dim)
    
    dirts = {}
    agents = {}
    options = {'grid_size':env.dim, 'auto_start':False}

    for l in f:
        s = "".join(l.split()).lower()
        if s == "":
            continue
        spl = s.split('=')
        if len(spl) != 2:
            raise MalformedVWFile("malformed line: " + l)
        print(spl)
        
        match_coord = re.match(r'^\(([0-9]+),([0-9]+)\)$', spl[0])
        if match_coord is not None:
            coord = (int(match_coord.group(1)), int(match_coord.group(2)))
            objspl = spl[1].split('_')
            if len(objspl) == 2 and objspl[1] == 'dirt':
                if vwc.is_colour(objspl[0]):
                    dirts[coord] = env.dirt(objspl[0])
                else:
                    raise MalformedVWFile('Invalid color:' + l)
                #env.replace_dirt(coord, dirt)
            if len(objspl) == 3 and objspl[2] == 'agent': #its and agent
                pass
                
                
                #agents[coord] =  env.agent(colour, direction)
        else:
            match_word = re.match(r'^[a-z_]+$', spl[0])
            if match_word is not None: 
                option = match_word.group(0)
                if option in VALID_OPTIONS:
                    try:
                        options[option] = VALID_OPTIONS[option](spl[1])
                    except:
                        raise MalformedVWFile('Option value invalid: ' + l)
                else:
                    raise MalformedVWFile('Invalid option: ' + l)
            else:
                raise MalformedVWFile('Invalid option: ' + l)
            
            
            
    env.reset(options['grid_size'])
    for c,a in agents.items():
        env.replace_agent(c,a)
    for c,d in dirts.items():
        env.replace_dirt(c,d)
    f.close()
    
