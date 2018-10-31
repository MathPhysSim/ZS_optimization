#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 21:30:16 2018

@author: shirlaen
"""
        #anodes
        #japc.setParam("ZS1.LSS2.MOTOR/Setting#downstreamAnodeSeptaPosition",x[0])
        #japc.setParam("ZS1.LSS2.MOTOR/Setting#upstreamAnodeSeptaPosition",x[0])         
        #japc.setParam("ZS2.LSS2.MOTOR/Setting#upstreamAnodeSeptaPosition",x[0])
        #japc.setParam("ZS2.LSS2.MOTOR/Setting#downstreamAnodeSeptaPosition",x[1])
        #japc.setParam("ZS3.LSS2.MOTOR/Setting#upstreamAnodeSeptaPosition",x[2])
        #japc.setParam("ZS3.LSS2.MOTOR/Setting#downstreamAnodeSeptaPosition",x[3])
        #japc.setParam("ZS4.LSS2.MOTOR/Setting#upstreamAnodeSeptaPosition",x[4])
        #japc.setParam("ZS4.LSS2.MOTOR/Setting#downstreamAnodeSeptaPosition",x[5])
        #japc.setParam("ZS5.LSS2.MOTOR/Setting#upstreamAnodeSeptaPosition",x[6])
        #japc.setParam("ZS5.LSS2.MOTOR/Setting#downstreamAnodeSeptaPosition",x[7])
        
        
        
        #girder
        #japc.setParam("ZS.LSS2.GIRDER/Setting#downstreamSeptaPosition",x[0])
class ListSelector():

    parameterList = { "ZS5 down":
                    {"name": "ZS5.LSS2.MOTOR/Setting#downstreamAnodeSeptaPosition",
                      "type": "scalar_constrained", 'startDirection': 0.3, 'limits' : [-2, 2]},
                    "ZS1 down":
                    {"name": "ZS1.LSS2.MOTOR/Setting#downstreamAnodeSeptaPosition",
                      "type": "scalar_constrained", 'startDirection': 0.3, 'limits' : [-2, 2]},
                    "ZS2 up":
                    {"name": "ZS2.LSS2.MOTOR/Setting#upstreamAnodeSeptaPosition",
                      "type": "scalar_constrained", 'startDirection': 0.3, 'limits' : [-2, 2]},
                    "ZS2 down":
                    {"name": "ZS2.LSS2.MOTOR/Setting#downstreamAnodeSeptaPosition",
                      "type": "scalar_constrained", 'startDirection': 0.3, 'limits' : [-2, 2]},
                     "ZS3 up":
                    {"name": "ZS3.LSS2.MOTOR/Setting#upstreamAnodeSeptaPosition",
                      "type": "scalar_constrained", 'startDirection': 0.3, 'limits' : [-2, 2]},
                     "ZS3 down":
                    {"name": "ZS3.LSS2.MOTOR/Setting#downstreamAnodeSeptaPosition",
                      "type": "scalar_constrained", 'startDirection': 0.3, 'limits' : [-2, 2]},
                     "ZS4 up":
                    {"name": "ZS4.LSS2.MOTOR/Setting#upstreamAnodeSeptaPosition",
                      "type": "scalar_constrained", 'startDirection': 0.3, 'limits' : [-2, 2]},
                     "ZS4 down":
                    {"name": "ZS4.LSS2.MOTOR/Setting#downstreamAnodeSeptaPosition",
                      "type": "scalar_constrained", 'startDirection': 0.3, 'limits' : [-2, 2]},
                     "ZS5 up":
                    {"name": "ZS5.LSS2.MOTOR/Setting#upstreamAnodeSeptaPosition",
                      "type": "scalar_constrained", 'startDirection': 0.3, 'limits' : [-2, 2]}
                    }
                    

    def getItems(self):
        return self.parameterList.keys()

    def getSelectedItemsNames(self):
        return [self.parameterList[key] for key in self.selectionList]

    def getSelectedItemsDict(self):
        return {key: self.parameterList[key] for key in self.selectionList}

    def __init__(self):
        self.selectionList = []
        
    def setSelection(self, selectedItems):
        self.selectionList = selectedItems
    
    def setItemTime(self, key, values):
        self.parameterList[key]["time"] = values
                          
    def setItemStartDirection(self, key, value):
        self.parameterList[key]["startDirection"] = value                      
        
        
