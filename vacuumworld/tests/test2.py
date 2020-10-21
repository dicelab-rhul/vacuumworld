# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 14:19:31 2019

author: Benedict Wilkins
"""
import sys
import inspect
from vacuumworld.vwutils import ignore

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
    
    def __print__(self, frame, event, arg):
        ignore(arg)

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
    
    def __enter__(self):
        sys.settrace(self.__trace__)
    
    def __exit__(self, *args):
        ignore(self)
        ignore(args)

        sys.settrace(None)
        
        
def test_c(*args):
    print( 'input =', *args)

def test_b(arg):
    val = arg * 5
    test_c(val)

def test_a():
    test_b(2)
    
TRACE_INTO = ['b']
with Trace():
   test_a() 
 