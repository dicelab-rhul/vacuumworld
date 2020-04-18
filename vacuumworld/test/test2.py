#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 14:19:31 2019

author: Benedict Wilkins
"""
import sys
import inspect

class Trace:
    
    def __init__(self):
        self.ignore_write = 0
        self._write = 'write'
        self._call = 'call'
        self._line = 'line'
        self._return = 'return'
    
    def __trace__(self, frame, event, arg):
        func_name = frame.f_code.co_name
        if event == self._call and func_name == self._write:
            self.ignore_write += 1
            return self.__trace__
        if event == self._return and func_name == self._write:
            self.ignore_write -= 1
            return
        
        if not self.ignore_write:
            return self.__print__(frame, event, arg)

        if event == self._call:
            return self.__trace__
        return
    
    def __print__(self, frame, event, arg):
        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno
        filename = co.co_filename
    
        if event == self._call:
            print('Call to %s on line %s of %s' % (func_name, line_no, filename))
            return self.__trace__
        elif event == self._return:
            print(inspect.getsourcelines(frame))
            print('Return %s on line %s' % (func_name, line_no))
        return
    
    def __enter__(self):
        sys.settrace(self.__trace__)
    
    def __exit__(self, *args):
        sys.settrace(None)
        
        
def c(*args):
    print( 'input =', *args)
    #print( 'Leaving c()')
    pass

def b(arg):
    val = arg * 5
    c(val)
    #print( 'Leaving b()')

def a():
    b(2)
    #print( 'Leaving a()')
    
TRACE_INTO = ['b']
with Trace():
   a() 
   
   

    
    
    
    
    
    
    
    