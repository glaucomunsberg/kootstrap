#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, os, argparse,sys

sys.path.append('../')

from system.Kootstrap import Kootstrap
from system.Metadata import Metadata
from system.Logger import Logger
from system.Helper import Helper

class Dataset:
    
    _k      = None
    _logger         = None
    _helper         = None
    _args           = None
    
    dataset_name    = None
    classes         = None
    dataset_path    = None
    dataset_md      = None
    
    def __init__(self,args,logger=None):
        
        self._k = Kootstrap()
        
        if logger == None:
            self._logger = Logger(app_name='Dataset')
        else:
            self._logger = logger
        
        self._helper= Helper()
        self._args  = args
        
        self.dataset_name = self.normalizeDatasetName(args.dataset_name)
        
        self.dataset_path = self._k.config['path_root']+self._k.config['path_dataset']+self.dataset_name+"/"
             
        self.classes    = []
        if args.classes_load_file != None:
            self.classes = self._helper.filePathToList(args.classes_load_file)
        else:
            self.classes = [x.replace('\n', '').replace('\r', '') for x in args.classes.split(",")]
            
    def start(self):
        
        if not os.path.exists(self.dataset_path):
            self._logger.info("Dataset: named has '{0}' was created".format(self.dataset_name))
            self._logger.info("Dataset: path'{0}'".format(self.dataset_path))
            os.makedirs(self.dataset_path)
            
            if not os.path.exists(self.dataset_path+"classes/"):
                self._logger.info("Dataset: create classes folder")
                os.makedirs(self.dataset_path+"classes/")
                
            if not os.path.exists(self.dataset_path+"subsets/"):
                self._logger.info("Dataset: create subsets folder")
                os.makedirs(self.dataset_path+"subsets/")
            
            self.dataset_md = Metadata(self.dataset_path+"metadata.json",True)
            self.dataset_md.metadata['name'] = self.dataset_name
            self.dataset_md.metadata['serial_identifier'] = self._helper.getSerialNow()
            self.dataset_md.metadata['created_at'] = self._helper.getTimeNow()
            self.dataset_md.metadata['classes'] = {}
            self.dataset_md.metadata['classes_order'] = self.classes
            self.dataset_md.metadata['kootstrap_version'] = self._k.config['version']
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
                self._logger.info("Dataset: Create subdirectory '{0}'".format("classes/"+class_name))
        
        self._logger.info("Dataset: end correctly")
        
    @staticmethod
    def normalizeDatasetName(name):
        name = re.sub('[^A-z0-9 -]', '', name)
        name = name.replace(" ","_")
        return name.lower()
    
    @staticmethod
    def isADatasetOrSubset(name):
        k       = Kootstrap()
        path    = None
        path_to = None
        path_datasets = k.path_dataset()
        datasets = [dI for dI in os.listdir(path_datasets) if os.path.isdir(os.path.join(path_datasets,dI))]
        for dataset in datasets:
            
            path_dataset = path_datasets+dataset+"/subsets/"
            #print 'dataset ', path_dataset
            if dataset == name:
                path    = path_dataset
                path_to = 'dataset'
                return path, path_to
            
            subsets = [dI for dI in os.listdir(path_dataset) if os.path.isdir(os.path.join(path_dataset,dI))]
            for subset in subsets:
                
                path_subset = path_dataset+subset+"/"
                #print 'subst ', path_subset
                if subset == name:
                    path    = path_subset
                    path_to = 'subset'
                    return path, path_to
        return path
    
    @staticmethod
    def normalizePathSubset(path):
        k = Kootstrap()
        absolut_path = path
        
        if absolut_path[:1] == ".":
            
            if absolut_path[-1:] == "/":
                absolut_path   = absolut_path[:-1]

            absolut_path = absolut_path.split("/")
            absolut_path = absolut_path[-3:]
            absolut_path = k.path_dataset()+absolut_path[0]+"/"+absolut_path[1]+"/"+absolut_path[2]
            
        else:
            
            if absolut_path.split("/") <= 3:
                
                name_subset     = absolut_path.split("/")[-1:]
                path_datasets   = k.path_dataset()
                
                datasets = [dI for dI in os.listdir(path_datasets) if os.path.isdir(os.path.join(path_datasets,dI))]
                
                for dataset in datasets:
                    subsets = [dI for dI in os.listdir(path_datasets) if os.path.isdir(os.path.join(path_datasets,dI))]
                    for subset in subsets:
                        if name_subset == subset:
                            #print 'Find subset at '+k.path_dataset()+dataset+"/"+subset+"/"
                            absolut_path = k.path_dataset()+dataset+"/"+subset+"/"
                
        return absolut_path
        