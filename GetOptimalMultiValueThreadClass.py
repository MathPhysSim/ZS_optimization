#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 10:48:23 2018

@author: shirlaen
"""
import os

import datetime
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import time
from scipy import optimize
import numpy as np
import pandas as pd


class CommuticatorSingals(QObject):

    drawNow = pyqtSignal()
    jobFinished = pyqtSignal()
    setValues = pyqtSignal(list)
    setSubscribtion = pyqtSignal(bool)
    showDataOK = pyqtSignal(str)


class Getoptimalmultivaluethread(QThread):

    def __init__(self, parameterClass, observableParameter, algorithmSelection,
                 xTol, fTol, xSmall, isSimulation):

        QThread.__init__(self)

        self.ob = observableParameter
        self.parameterClass = parameterClass
        index = self.parameterClass.getNames()
        index.append("intensity")
        
        self.parameterEvolution = pd.DataFrame(
                index=index)
        self.limits = self.parameterClass.get_limits()
        
        self.cancelFlag = False
        self.signals = CommuticatorSingals()
        self.nrCalls = 0
        self.startValues = np.array(self.parameterClass.getStartVector())
        self.save_path = 'saved_data/'
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        self.store_name = '{0}{1}.csv'.format(self.save_path, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        self.updateData(self.startValues, np.nan)

        self.xTol = xTol
        self.fTol = fTol
        self.xSmall = xSmall
        self.algorithmSelection = algorithmSelection
        self.isSimulation = isSimulation
        self.limit_feedback_value = 5



    def updateData(self, x, intensityValue):
        # print('set values', x)
        self.parameterEvolution[self.nrCalls] = np.nan
        self.parameterEvolution.iloc[:-1,
                                     self.nrCalls] = np.array(x).flatten()
        self.parameterEvolution.iloc[-1,
                                     self.nrCalls] = intensityValue
        # print('values: ', self.parameterEvolution + self.parameterEvolution.iloc[0,:])
        self.parameterEvolution.to_csv(self.store_name)

    def __del__(self):
        self.wait()

    def run(self):

        self.signals.setSubscribtion.emit(True)
        x0 = self.startValues
        print(self.startValues)
        
        if self.algorithmSelection == 'Powell':
            res = optimize.fmin_powell(self._func_obj, x0, xtol=self.xTol,
                                      ftol=self.fTol,
                                      direc=self.parameterClass.
                                      getStartDirection())
            #res = optimize.minimize(self._func_obj, x0, method='powell',options={'disp': True,'direc':np.array([[0.3,0,0,0],[0,0.3,0,0],[0,0,0.3,0],[0,0,0,0.3]]),'ftol':0.5,'xtol':0.3})
            if (len(res.shape) < 0) | (type(res) == float):
                res = np.array([res])
#            returnValue = res
        else:
            res = optimize.minimize(self._func_obj, x0, method='Nelder-Mead',
                                    options={'xatol': self.xTol,
                                             'fatol': self.fTol})
#            returnValue = res.x
#        self.signals.setValues.emit(returnValue.tolist())
        #print(self.xTol, self.fTol)
        print(self.parameterEvolution)
        self.signals.showDataOK.emit("Acquisition ok?")
        self.signals.jobFinished.emit()
        self.signals.setSubscribtion.emit(False)

    def _func_obj(self, x):
        print('Inside _func_obj', x)
        limit_crossed = False

        if self.nrCalls > 1:
            pervious_settings = self.parameterEvolution.iloc[:-1, self.nrCalls]
            small_change = np.allclose(x, pervious_settings, atol=self.xSmall)
        else:
            small_change = False
  
        for i in range(len(x)):
            if not(np.isnan(self.limits[i]).any()):
                if (x[i]<self.limits[i][0])|(x[i]>self.limits[i][1]):
                    limit_crossed = True

        if not(small_change):
            self.signals.setValues.emit(x.tolist())

        if not(limit_crossed):
            print("_func_obj1")
            # In case of a small change
            if small_change:
                print(5*"small change")

                previous_observation = self.parameterEvolution.iloc[:,self.nrCalls]
                print('previous value', previous_observation)
                dataFinal = previous_observation.iloc[-1]

                # self.nrCalls += 1
                # self.updateData( previous_observation.iloc[:-1], dataFinal)
                # self.signals.drawNow.emit()
                # time.sleep(.1)
                return dataFinal
                self.signals.showDataOK.emit("Small")
            else:
                #In case of real data
                if( not(self.isSimulation)):
                    self.ob.reset()
                    while(self.ob.dataWait):
                        if self.cancelFlag:
                            self.signals.setSubscribtion.emit(False)
                            self.terminate()
                        time.sleep(2)
                    self.ob.dataWait = True

                    dataFinal = self.ob.dataOut
                    self.nrCalls += 1
                    self.updateData(x, dataFinal)
                else:
                    time.sleep(1)
                    if self.cancelFlag:
                        self.signals.setSubscribtion.emit(False)
                        self.signals.showDataOK.emit("Acquisition ok?")
                        self.terminate()
                    dataFinal = self.simulateObservable(x)
                    self.nrCalls += 1
                    self.updateData(x, dataFinal)

                self.signals.drawNow.emit()
                self.signals.showDataOK.emit("OK")
                return dataFinal
        else:
            print(25*"!Limit!!!")
            self.signals.showDataOK.emit("!Limit!!!")
            return self.limit_feedback_value
    
    def simulateObservable(self, x):
        print('simulateObservable x', x)
        offset = 1.
        
        A0 = np.array([5.,4.,3.,1.,0.5])
        b0 = [0.5,0.5,0.5,0.5,0.5]
        
        #print("comp ",compareArray)
        
        y = offset
        for i in range(len(x)):
               
            y=y+A0[i]*(x[i]-b0[i])*(x[i]-b0[i])
        
        #TODO: still need to randomise y
        print("y",y)
        return y
        
