# -*- coding: utf-8 -*-
from pystar.Perception import Perception

#maybe we use this... who knows!
class ActionResultPerception(Perception):
    
    def __init__(self,agid,action,result):
        super().__init__(agid)
        self.__actionAttempted__=action
        self.__result__=result   
     
    def getResult(self):
        return self.__result__
    
    def getActionAttempted(self):
        return self.__actionAttempted__
    