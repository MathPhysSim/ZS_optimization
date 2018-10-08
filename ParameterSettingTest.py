#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 22:37:51 2018

@author: shirlaen
"""

import numpy as np
import pyjapc
import ParameterSetting as pc

import ListSelectorClass as lsclass


japc = pyjapc.PyJapc(incaAcceleratorName="SPS", noSet=False)
japc.setSelector("SPS.USER.SFTPRO2")
parameterClass = pc.ParameterClass(japc)


ls = lsclass.ListSelector()
ls.setSelection(["ZS5 down"])
# japc.rbacLogin(loginDialog=True)
parameterClass.addParameters(ls.getSelectedItemsDict())
print("Current Value")
print(parameterClass.getValues())
setValue = parameterClass.getValues()
parameterClass.setNewValues((setValue))
print(parameterClass.getValues())