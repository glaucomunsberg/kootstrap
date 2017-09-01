#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, os, argparse,sys

sys.path.append('../')

from system.Koopstrap import Koopstrap
from system.Metadata import Metadata
from system.Logger import Logger
from system.Helper import Helper

class Dataset:
    
    _koopstrap      = None
    _logger         = None
    _helper         = None
    _args           = None
    
    dataset_name    = None
    classes         = None
    dataset_path    = None
    dataset_md      = None
    
    def __init__(self,args,logger=None):
        
        self._koopstrap = Koopstrap()
        
        if logger == None:
            self._logger = Logger(app_name='Dataset')
        else:
            self._logger = logger
        
        self._helper = Helper()
        
        #self.dataset_name = re.sub('[^A-z0-9 -]', '', args.dataset_name)
        #self.dataset_name = self.dataset_name.replace(" ","_")
        self.dataset_name = self.normalizeDatasetName(args.dataset_name)
        
        self.dataset_path = self._koopstrap.config['path_root']+self._koopstrap.config['path_dataset']+self.dataset_name+"/"
             
        self.classes    = []
        if args.classes_load_file != None:
            file = open(args.classes_load_file,'r')
            for line in file:
                self.classes.append(line.replace('\n', '').replace('\r', ''))
        else:
            self.classes = [x.replace('\n', '').replace('\r', '') for x in args.classes.split(",")]
            
    def start(self):
        
        if not os.path.exists(self.dataset_path):
            self._logger.info("Dataset: name '{0}' created".format(self.dataset_name))
            os.makedirs(self.dataset_path)
            
            if not os.path.exists(self.dataset_path+"classes/"):
                self._logger.info("Dataset: create classes folder")
                os.makedirs(self.dataset_path+"classes/")
                
            if not os.path.exists(self.dataset_path+"subsets/"):
                self._logger.info("Dataset: create subsets folder")
                os.makedirs(self.dataset_path+"subsets/")
            
            self.dataset_md = Metadata(self.dataset_path+"metadata.json",True)
            self.dataset_md.metadata['name'] = self.dataset_name
            self.dataset_md.metadata['created_at'] = self._helper.getTimeNow()
            self.dataset_md.metadata['classes'] = {}
            self.dataset_md.metadata['annotation'] = self._args.annotation
            self.dataset_md.save()
        else:
            self.dataset_md = Metadata(self.dataset_path+"metadata.json")
            
        for class_name in self.classes:
            class_name = class_name
            self._logger.info("Dataset: created classe '{0}'".format(class_name))
            if not os.path.exists(self.dataset_path+"classes/"+class_name):
                os.makedirs(self.dataset_path+"classes/"+class_name)
                self.dataset_md.metadata['classes'][class_name] = {}
                self.dataset_md.metadata['classes'][class_name]['num_images'] = 0
                self.dataset_md.metadata['classes'][class_name]['images'] = []
            self.dataset_md.save()
        
        self._logger.info("Dataset: end correctly")
        
    @staticmethod
    def normalizeDatasetName(name):
        name = re.sub('[^A-z0-9 -]', '', name)
        return name.replace(" ","_")
        