#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 14:19:31 2019

author: Benedict Wilkins
"""
import sys
import inspect
import traceback


class TraceFrames:
    
    def __init__(self):
        self.ignore_write = 0
        self.frames = [None]
        self.calls = []
        self.returns = []
        
        self._write = 'write'
        self._call = 'call'
        self._line = 'line'
        self._return = 'return'

    
    def __trace__(self, frame, event, arg):
        func_name = frame.f_code.co_name
        if event == self._line:
            #print('line', func_name)
            return self.__trace__

        if event == self._call and func_name == self._write:
            self.ignore_write += 1
            return self.__trace__
        if event == self._return and func_name == self._write:
            self.ignore_write -= 1
            return
        
        if not self.ignore_write:
            return self.__record__(frame, event, arg)

        if event == self._call:
            return self.__trace__
        return
    
    def __record__(self, frame, event, arg):
        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno
        filename = co.co_filename

        if event == self._call:
            #print('Call to %s on line %s of %s' % (func_name, line_no, filename))
            if self.frames[-1] != frame:
                self.frames.append(frame)
            self.calls.append((func_name, line_no, filename))    
            
            return self.__trace__
        elif event == self._return:
            #print('Return %s on line %s' % (func_name, line_no))
            self.returns.append((func_name, line_no, filename))
        return
    
    def __enter__(self):
        try:
            sys.settrace(self.__trace__)
        except:
            #dont know when this might happen...?
            print("FAILED TO SET TRACE")
            traceback.print_exc()
    
    def __exit__(self, *args):
        sys.settrace(None)
        self.frames = self.frames[1:-1]
        self.calls = self.calls[:-1]
        
    def formatted(self):
        f =  "Causes by:\n"
        for fun, line, file in self.calls:
            f += "File {0}, line {1} in {2}\n".format(file, str(line), fun)
        
        
        return f




class Trace:
    
    def __init__(self):
        self.ignore_write = 0
        self.frames = [None]
        self.calls = []
        self.returns = []
        
        self._write = 'write'
        self._call = 'call'
        self._line = 'line'
        self._return = 'return'

    
    def __trace__(self, frame, event, arg):
        func_name = frame.f_code.co_name
        if event == self._line:
            #print('line', func_name)
            return self.__trace__

        if event == self._call and func_name == self._write:
            self.ignore_write += 1
            return self.__trace__
        if event == self._return and func_name == self._write:
            self.ignore_write -= 1
            return
        
        if not self.ignore_write:
            return self.__record__(frame, event, arg)

        if event == self._call:
            return self.__trace__
        return
    
    def __record__(self, frame, event, arg):
        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno
        filename = co.co_filename

        if event == self._call:
            #print('Call to %s on line %s of %s' % (func_name, line_no, filename))
            if self.frames[-1] != frame:
                self.frames.append(frame)
            self.calls.append((func_name, line_no, filename, arg))    
            
            return self.__trace__
        elif event == self._return:
            #print('Return %s on line %s' % (func_name, line_no))
            self.returns.append((func_name, line_no, filename, arg))
        return
    
    def __enter__(self):
        try:
            sys.settrace(self.__trace__)
        except:
            #dont know when this might happen...?
            print("FAILED TO SET TRACE")
            traceback.print_exc()
    
    def __exit__(self, *args):
        sys.settrace(None)
        self.frames = self.frames[1:-1]
        self.calls = self.calls[:-1]
        
    def formatted(self):
        f =  "Causes by:\n"
        for fun, line, file in self.calls:
            f += "File {0}, line {1} in {2}\n".format(file, str(line), fun)
        
        
        return f
    
    
    
    
        
def c(*args):
    return None

def b(arg):
    val = arg * 5
    return c(val)
    #print( 'Leaving b()')

def decide():

    test = lambda x: x + 1
    test(1)
    
    return b(2)
    #print( 'Leaving a()')
    
TRACE_INTO = ['b']



def cycle():
    trace = Trace()

    with trace:
        a = decide()

    for frame in trace.frames: #ignore None the __exit__ frame
        print(frame, inspect.getsourcelines(frame))
    
    for call in trace.calls:
        print(call)
        
    for ret in trace.returns:
        print(ret)

'''
class ActionError(Exception):
    # All who inherit me shall not traceback, but be spoken of cleanly
    pass

def quiet_hook(kind, message, traceback):
    print("hook")
    if ActionError in kind.__bases__:
        print('{0}: {1}'.format(kind.__name__, message))  # Only print Error Type and Message
    else:
        pass
        sys.__excepthook__(kind, message, traceback)  # Print Error Type, Message and Traceback

sys.excepthook = quiet_hook #doesnt ork for ipython...
'''

cycle()
  
    
    


