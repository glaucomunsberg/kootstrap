#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, sys

sys.path.append('../')

from system.Kootstrap import Kootstrap

class Model:
    
    def __init__(self,args,logger=None):
        None
        
    @staticmethod
    def normalizeModelName(name):
        name = re.sub('[^A-z0-9 -]', '', name)
        return name.replace(" ","_")
        
    @staticmethod
    def pathFromModelName(name):
        k       = Kootstrap()
        path    = None
        path_to = None
        path_models = k.path_model()
        models = [dI for dI in os.listdir(path_models) if os.path.isdir(os.path.join(path_models,dI))]
        for model in models:
            
            path_model = path_models+model+"/"
            if model == name:
                path    = path_model
                
        return path