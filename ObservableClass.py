#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 14:41:13 2018

@author: shirlaen
"""

import numpy as np


class ObservableClass():

    def __init__(self, japc, length=5):
        self.valueList = []
        self.japc = japc
        self.dataOut = False
        self.dataWait = True
        self.dataLength = length
        self.method = 'Method 1'
        self.timeInterval = np.array([0, 0])
        self.required_x = []
        
    def compareSettings(self, x):
        #print("Acquire position: ", self.japc.getParam("ZS.LSS2.GIRDER/Acquisition#downstreamSeptaPosition_meas"))
        if((x[0]+0.1)>self.japc.getParam("ZS.LSS2.GIRDER/Acquisition#downstreamSeptaPosition_meas") and (x[0]-0.1)<self.japc.getParam("ZS.LSS2.GIRDER/Acquisition#downstreamSeptaPosition_meas") ):
           return True
        else:
            return False
                  
    def setValue(self, newValue):

        extracted_intensity = np.nan 
        beam_loss = np.nan
        
        if(newValue["userName"]=="SPS.USER.SFTPRO1"):
            #if(self.compareSettings(self.required_x)):
            if(newValue["extractedIntensity"]>5e8):
                extracted_intensity = newValue["extractedIntensity"]
                beam_loss =0.0
                lossRange = np.arange(6)
                for i,val in enumerate(lossRange):
                    beam_loss = beam_loss + self.japc.getParam("BLRSPS_LSS2/Acquisition#calLosses")[i]*1000.
                #beam_loss = self.japc.getParam("BLRSPS_LSS2/Acquisition#calLosses")[2]*1000.
            self.dataWait = False                                       
        observable_value = (beam_loss/extracted_intensity)*1.e+10
        #print("passed")
        if self.method == 'Method 1':
            self.dataOut = observable_value
        elif self.method == 'Method 2':
            self.dataOut = observable_value

    def reset(self):
        self.valueList = []
