#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 15:49:45 2019

@author: ben
"""

from time import perf_counter, sleep, time

import time


t = lambda: int(round(time.time() * 1000))

    
class Clock:
    
    def __init__(self, fps):
        self.start = perf_counter()
        self.frame_length = 1/fps
        
    @property
    def tick(self):
        return (perf_counter() - self.start)/self.frame_length

    def sleep(self):
        r = self.tick + 1
        while self.tick < r:
            sleep(1/1000)   
            
c = Clock(60)

t1 = t()
with Sleep(0.1):
    pass
print(t() - t1)