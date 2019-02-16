#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, json, sys, os
sys.path.append('../')

from keras.models import model_from_json

from system.Kootstrap import Kootstrap
from system.Metadata import Metadata
from system.Logger import Logger
from system.Helper import Helper
from maker.Dataset import Dataset
from trainer.Model import Model

class Mananger:
    
    _k          = None
    _logger     = None
    _helper     = None
    _args       = None
    
    model       = None
    test_md     = None
    
    model_name          = None
    model_md            = None
    path_model          = None
    path_model_json     = None
    path_model_weights  = None
    path_set            = None
    dataset_set_type    = None
    set_name            = None
    set_md              = None
    path_load_set       = None
    path_test           = None
    classes_order       = None
    
    path_test_predictions_file  = None
    test_predictions_csv        = None
    
    def __init__(self,args,logger=None):
        
        self._k         = Kootstrap()
        self._helper    = Helper()
        
        if logger == None:
            self._logger = Logger('Mananger')
        else:
            self._logger = logger
            
        self._args      = args
        
        # select the model by name
        if args.model_name == None:
            raise ValueError('arg --model_name need by setted')
        else:
            self.model_name = Model.normalizeModelName(args.model_name)
            self.path_model = Model.pathFromModelName(self.model_name)
            
        if self.model_name == None:
            raise ValueError('arg --model_name is not a valid url or name')
            
        if self.path_model == None:
            raise ValueError('arg --model_name is not a valide model path')
        
        self.model_md   = Metadata(self.path_model+"metadata.json")
        
        # select the weights
        if args.epoch == -1:
            self.path_model_weights = self.path_model+"weights/weights.h5"
        else:
            self.path_model_weights = self.path_model+"weights/weights_epoch_%03d.h5" % args.epoch
            
        if not os.path.isfile(self.path_model_weights):
            raise ValueError('arg --epoch is not a valid weights to by used')
            
        self.path_model_json = self.path_model+"model.json"
        
        if not os.path.isfile(self.path_model_json):
            raise ValueError('We can\'t load the model from your trainning')
            
        # select the path from dataset
        self.set_name           = args.load_data
        path_and_type_dataset   = Dataset.isADatasetOrSubset(self.set_name)
        
        if args.load_data== None: #args.load_subset == None and args.load_dataset == None:
            raise ValueError('you need send the name or path to dataset or subset')
        elif path_and_type_dataset == None:
            raise ValueError('the name of dataset or subset is not valid')
        else:
            
            self.path_set           = path_and_type_dataset[0]
            self.dataset_set_type   = path_and_type_dataset[1]
            
            self.path_load_set = Dataset.normalizePathSubset(self.path_set)
            
            if self.dataset_set_type == 'subset':
        
                #get final to create the absolute path
                self.set_md = Metadata(self.path_load_set+"metadata.json")
                
                self._logger.info("Mananger: subset {0} form dataset{1} created at {2}".format(self.set_md.metadata['name'],self.set_md.metadata['parental_name'],self.set_md.metadata['created_at']))
            else:
                #get final to create the absolute path
                self.set_md = Metadata(self.path_load_set+"metadata.json")
                self._logger.info("Mananger: Dataset {0} created at {2}".format( self.set_md.metadata['name'], self.set_md.metadata['created_at']))
                
            
        if self.dataset_set_type == 'subset' and not args.set in ["train","validation","test"]:
            raise ValueError('arg --set is not a valid set on dataset or subset')
            
        if self.dataset_set_type == 'subset':
            self.path_load_set += args.set+"/"
        else:
            self.path_load_set += "classes/"
            
        if not os.path.isdir(self.path_load_set):
            raise ValueError('args --load_data and --set is not a valid  to by used')
        
        serial_identifier   = self._helper.getSerialNow()
        
        if args.test_name == None:
            self.path_test      = self._k.path_test()+self.model_name+"/"+serial_identifier+"_"+self.set_name+"/"
        else:
            self.path_test      = self._k.path_test()+self.model_name+"/"+args.test_name+"/"
            
        os.makedirs(self.path_test)
        
        self.test_md = Metadata(self.path_test+"metadata.json",True)
        
        self.test_md.metadata['serial_identifier']  = serial_identifier
        self.test_md.metadata['created_at']         = self._helper.getTimeNow()
        self.test_md.metadata['model']              = self.model_name
        self.test_md.metadata['weigths']            = self.path_model_weights.split("/")[-1:][0]
        
        if self.dataset_set_type == 'subset':
            self.test_md.metadata['dataset']= self.set_md.metadata['parental_name']
            self.test_md.metadata['subset'] = self.set_md.metadata['name']
            self.test_md.metadata['set']    = args.set
        else:
            self.test_md.metadata['dataset']= self.set_md.metadata['name']
            self.test_md.metadata['subset'] = ""
            self.test_md.metadata['set']    = ""
            
        self.test_md.metadata['num_classes']= len(self.set_md.metadata['classes_order'])
        self.test_md.metadata['annotation'] = args.annotation
        self.test_md.metadata['start_at']   = ""
        self.test_md.metadata['end_at']     = ""
        self.test_md.save()
        
        
        # prediction set
        self.path_test_predictions_file = self.path_test+"predictions.csv"
        self.test_predictions_csv       = open(self.path_test_predictions_file, 'w')
        self.classes_order              = self.set_md.metadata['classes_order']
        
        prediction_header = "class origem;image name;"
        for class_name in self.classes_order:
            prediction_header+=class_name+";"
            
        prediction_header+= os.linesep
        self.test_predictions_csv.write(prediction_header)
        
        print 'self.path_set', self.path_set
        print 'model name', self.model_name
        print 'model path', self.path_model
        print 'self.path_load_set', self.path_load_set    
        
    def setModel(self,model):
        
        self.model = model
        
    def getModelWithWeights(self,model=None):
        if model == None:
            model = self.model
            
        try:
            json_file = open(self.path_model_json, 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            model = model_from_json(loaded_model_json)
            self._logger.info('Mananger: Loading model at '+self.path_model_json)
        except:
            self._logger.error('Mananger: Error at loading model from file '+str(self.path_model_json))
        
        self._logger.info('Mananger: loading model from file: '+self.path_model_weights)
        model.load_weights(self.path_model_weights)
        return model