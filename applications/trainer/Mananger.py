#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, keras, os, glob, traceback
sys.path.append('../')

from keras.models import Model, model_from_json
from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19
from keras.preprocessing import image

from system.Kootstrap import Kootstrap
from system.Metadata import Metadata
from system.Logger import Logger
from system.Helper import Helper
from maker.Dataset import Dataset
from Callbacks import KCallback

class Mananger:
    
    _k          = None
    _subset_md  = None
    _logger     = None
    _helper     = None
    _args       = None
    
    model               = None
    model_name          = None
    metadata            = None
    
    path_load_subset    = None
    path_model          = None
    path_model_test     = None
    path_model_file     = None
    path_model_weights_file = None
    
    path_dataset        = None
    dataset_set_type    = None
    files_attached_md   = None
    
    def __init__(self,args,logger=None):
        
        self._k         = Kootstrap()
        self._helper    = Helper()
        
        if logger == None:
            self._logger = Logger('Mananger')
        else:
            self._logger = logger
            
        self._args      = args
        serial_identifier   = self._helper.getSerialNow()
        
        if args.load_model_file != None:
            if not os.path.exists(args.load_model_file):
                raise ValueError('arg --load_model_file is not a valid file .json')
            else:
                if self.model_name != None:
                    self.model_name = Dataset.normalizeDatasetName(serial_identifier)
                else:
                    self.model_name = Dataset.normalizeDatasetName(args.model_name)
        else:
            self.model_name         = Dataset.normalizeDatasetName(args.model_name)
            
        self.path_model = self._k.path_model() + self.model_name+"/"
        
        self.path_model_test            = self._k.path_test() + self.model_name+"/"
        self.path_model_file            = self._k.path_model()+ self.model_name+"/model.json"
        self.path_model_files_attached  = self._k.path_model()+ self.model_name+"/files_attached.json"
        self.path_model_weights_file    = self._k.path_model()+ self.model_name+"/weights/weights.h5"
                
        if args.model_name == None and args.load_model_file == None:
            raise ValueError('both args --model_name and --load_model_file are empty.Create a model or load')
            
        if self._args.load_weights != None and not os.path.exists(self._args.load_weights):
                raise ValueError('arg --load_weights is not a valid file .h5')
                
        path_and_type_dataset   = Dataset.isADatasetOrSubset(args.load_data)
        
        if args.load_data== None: #args.load_subset == None and args.load_dataset == None:
            raise ValueError('you need send the name or path to data train')
        elif path_and_type_dataset == None:
            raise ValueError('the name of dataset or subset is not valid')
        else:
            
            self.path_dataset       = path_and_type_dataset[0]
            self.dataset_set_type   = path_and_type_dataset[1]
            
            self.path_load_subset = Dataset.normalizePathSubset(self.path_dataset)
            
            if self.dataset_set_type == 'subset':
        
                #get final to create the absolute path
                self._subset_md = Metadata(self.path_load_subset+"metadata.json")
                
                self._logger.info("Mananger: subset {0} form dataset{1} created at {2}".format(self._subset_md.metadata['name'],self._subset_md.metadata['parental_name'],self._subset_md.metadata['created_at']))
                self._logger.info("Mananger: train size {0}, validation size {1} and test size {2}".format(self._subset_md.metadata['train_proporcional_size'],self._subset_md.metadata['validation_proporcional_size'],self._subset_md.metadata['test_proporcional_size']))
            else:
                #get final to create the absolute path
                self._subset_md = Metadata(self.path_load_subset+"metadata.json")
                self._logger.info("Mananger: Dataset {0} created at {2}".format(self._subset_md.metadata['name'],self._subset_md.metadata['created_at']))
                self._logger.info("Mananger: train size total")
                    
        if not os.path.exists(self.path_model):
            self._logger.info("Mananger: create a model '{0}' at '{1}' ".format(self.model_name, self.path_model))
            os.makedirs(self.path_model)
            os.makedirs(self.path_model+"/weights/")
            self.model_md = Metadata(self.path_model+"metadata.json", True)
        else:
            self.model_md = Metadata(self.path_model+"metadata.json")
            
        if not os.path.exists(self.path_model_test):
            self._logger.info("Mananger: create test dir to model '{0}' at '{1}' ".format(self.model_name, self.path_model_test))
            os.makedirs(self.path_model_test)
            
        if not os.path.isfile(self.path_model_files_attached):
            self._logger.info("Mananger: create files attached '{0}' ".format(self.path_model_files_attached))
            self.files_attached_md = Metadata(self.path_model_files_attached,True)
            self.files_attached_md.metadata['train_images'] = {}
            self.files_attached_md.metadata['validation_images'] = {}
            self.files_attached_md.save()
        else:
            self.files_attached_md = Metadata(self.path_model_files_attached)

        self.model_md.metadata['name']              = self.model_name
        self.model_md.metadata['serial_identifier'] = serial_identifier
        self.model_md.metadata['path_dataset']      = self.path_dataset
        self.model_md.metadata['created_at']        = self._helper.getTimeNow()
        self.model_md.metadata['history_loss']      = []
        self.model_md.metadata['history_acc']       = []
        self.model_md.metadata['time_elapsed']      = []
        self.model_md.metadata['model_layers']      = []
        self.model_md.metadata['active']            = False
        self.model_md.metadata['begin_at']          = "-"
        self.model_md.metadata['end_at']            = "-"
        if self._args.epochs > 0:
            self.model_md.metadata['epoch_total']   = self._args.epochs
        else:
            self.model_md.metadata['epoch_total']   = self._k.trainer['epochs_total']
        self.model_md.metadata['epoch_current'] = 0
        self.model_md.metadata['classes_number']= len(self._subset_md.metadata['classes_order'])
        self.model_md.metadata['classes']       = self._subset_md.metadata['classes_order']
        self.model_md.metadata['annotation']    = self._args.annotation
        
        if self.dataset_set_type == 'dataset':
            self.model_md.metadata['train_type']        = 'dataset'
            self.model_md.metadata['train_dataset_name']= self._subset_md.metadata['name']
            self.model_md.metadata['train_subset_name'] = ""
        else:
            self.model_md.metadata['train_type']        = 'subset'
            self.model_md.metadata['train_dataset_name']= self._subset_md.metadata['parental_name']
            self.model_md.metadata['train_subset_name'] = self._subset_md.metadata['name']
            
        if self._args.load_weights != None:
            self.model_md.metadata['load_weights']      = True
            self.model_md.metadata['load_weights_path'] = self._args.load_weights
        else:
            self.model_md.metadata['load_weights']      = False
            self.model_md.metadata['load_weights_path'] = ""
            
        self.model_md.metadata['target_size']   = self._k.trainer['target_size']
        self.model_md.metadata['batch_size']    = self._k.trainer['batch_size']
        self.model_md.metadata['target_acc']    = self._k.trainer['target_acc']
        self.model_md.metadata['target_loss']   = self._k.trainer['target_loss']
        self.model_md.metadata['target_loss']   = self._k.trainer['target_loss']
        self.model_md.metadata['save_weights_to_each']  = self._k.trainer['save_weights_to_each']
        self.model_md.metadata['train_path']        = ""
        self.model_md.metadata['validation_path']   = ""
        self.model_md.metadata['valitation_steps_per_epoch']= 0
        self.model_md.metadata['train_steps_per_epoch']     = 0
        self.model_md.metadata['keras_version']     = keras.__version__
        self.model_md.metadata['kootstrap_version'] = self._k.version()
        self.model_md.save()
        
        self._logger.info("Mananger: _epoch_total         value {0}".format(self.model_md.metadata['epoch_total']))
        self._logger.info("Mananger: _batch_size          value {0}".format(self.model_md.metadata['batch_size']))
        self._logger.info("Mananger: _number_of_classes   value {0}".format(self.model_md.metadata['classes_number']))
        self._logger.info("Mananger: _train_type          value {0}".format(self.model_md.metadata['train_type']))
        self._logger.info("Mananger: _dataset             value {0}".format(self.model_md.metadata['train_dataset_name']))
        self._logger.info("Mananger: _subset              value {0}".format(self.model_md.metadata['train_subset_name']))
        self._logger.info("Mananger: _acc_target          value {0}".format(self.model_md.metadata['target_acc']))
        self._logger.info("Mananger: _loss_target         value {0}".format(self.model_md.metadata['target_loss']))
        self._logger.info("Mananger: _load_weights        value {0}".format(self.model_md.metadata['load_weights']))
        self._logger.info("Mananger: _load_weights_path   value {0}".format(self.model_md.metadata['load_weights_path']))
            
    def getModel(self,model=None):
        
        if model != None:
            self.model = model
        else:
            if self._args.load_model_file != None:
                try:
                    json_file = open(self._args.load_model_file, 'r')
                    loaded_model_json = json_file.read()
                    json_file.close()
                    self.model = model_from_json(loaded_model_json)
                    self._logger.info('Mananger: Loading model at '+self._args.load_model_file)
                except:
                    self._logger.error('Mananger: Error at loading model from file '+str(self._args.load_model_file))
                    self._logger.error(traceback.format_exc())
            else:
                if self._k.trainer['model'] == "VGG16":
                    self.model = VGG16(weights= self._k.trainer['weights'], include_top= self._k.trainer['include_top'])
                    
                elif self._k.trainer['model'] == "VGG19":
                    self.model = VGG19(weights= self._k.trainer['weights'], include_top= self._k.trainer['include_top'])
                else:
                    # Need by implemented
                    self._logger.info("Mananger: Model {0} not implemented yet!".format(self._k.trainer['model']))
                    raise ValueError("Mananger: Model {0} not implemented yet!".format(self._k.trainer['model']))
                    
                self._logger.info("Mananger: Loading {0} model".format(self._k.trainer['model']))
                
        if self._args.load_weights != None:
            self.model.load_weights(self._args.load_weights)
            self._logger.info('Centauri: Loading weights from file: '+self._args.load_weights)
                
        return self.model
    
    def getCallbacks(self,model=None):
        callbacks = []
        
        if model == None:
            model = self.model
            
        callbacks.append(KCallback(self.model,self.model_md,self._logger))
        return callbacks
    
    def printModel(self,model=None):
        if model == None:
            model = self.model
        self._logger.info('Mananger: print model')
        print model.summary()
        for i, layer in enumerate(model.layers):
            print(i, layer.name, layer.get_config())
            self._logger.info("Mananger: Layer {0} name '{1}'".format(i,layer.name))
        
    def save(self,model):
        self.saveWeights(model)
        self.saveModel(model)
        
    def saveWeights(self,model=None):
        if model == None:
            model = self.model
        model.save_weights(self.path_model_weights_file)
        self._logger.info("Mananger: Saving weitghts at {0}".format(self.path_model_weights_file))
        
    def saveModel(self,model=None):
        if model == None:
            model = self.model
        model_json = model.to_json()
        with open(self.path_model_file, "w") as json_file:
            json_file.write(model_json)
        self._logger.info("Mananger: Saving model.json at {0}".format(self.path_model_file))
        
    def configFitGenerator(self,datagen_train=None,datagen_validation=None):
        
        generator_train         = None
        generator_validation    = None
        
        if datagen_train == None:
            datagen_train = image.ImageDataGenerator(rescale=0) # (rescale=1./255, shear_range=0.2, zoom_range=0.2)
            
        if datagen_validation == None:
            datagen_validation = image.ImageDataGenerator(rescale=0)
            
            
        if self.model_md.metadata['train_type'] == 'dataset':
            path_directory_train        = self.path_load_subset+"classes/"
            path_directory_validation   = None
            
        else:
            path_directory_train        = self.path_load_subset+"train/"
            path_directory_validation   = self.path_load_subset+"validation/"
        
        # create generators
        generator_train = datagen_train.flow_from_directory(path_directory_train, target_size=(self.model_md.metadata['target_size'], self.model_md.metadata['target_size']), batch_size= self.model_md.metadata['batch_size'], class_mode='categorical', shuffle=self._k.trainer['shuffle'], classes=self._subset_md.metadata['classes_order'])
        
        if path_directory_validation != None:
            generator_validation = datagen_validation.flow_from_directory(path_directory_validation, target_size=(self.model_md.metadata['target_size'], self.model_md.metadata['target_size']), batch_size= self.model_md.metadata['batch_size'], class_mode='categorical', shuffle=self._k.trainer['shuffle'], classes=self._subset_md.metadata['classes_order'])
            
        # calc steps per epoch to train and validation sets
        total_images = 0
        steps_per_epoch_validation  = None
        steps_per_epoch_train       = 0
        
        for class_dir in self._subset_md.metadata['classes_order']:
            files = glob.glob(path_directory_train+class_dir+"/*.*")
            if not class_dir in self.files_attached_md.metadata['train_images']:
                self.files_attached_md.metadata['train_images'][class_dir] = []
            for file in files:
                self.files_attached_md.metadata['train_images'][class_dir].append(os.path.basename(file))
            total_images += len(files)
        steps_per_epoch_train = total_images
        self.model_md.metadata['train_path']            = path_directory_train
        self.model_md.metadata['train_steps_per_epoch'] = steps_per_epoch_train
        
        if path_directory_validation != None:
            total_images = 0
            classes_dirs = self._subset_md.metadata['classes_order']
            for class_dir in classes_dirs:
                files = glob.glob(path_directory_validation+class_dir+"/*.*")
                if not class_dir in self.files_attached_md.metadata['validation_images']:
                    self.files_attached_md.metadata['validation_images'][class_dir] = []
                for file in files:
                    self.files_attached_md.metadata['validation_images'][class_dir].append(os.path.basename(file))
                total_images += len(files)
            steps_per_epoch_validation = total_images
            self.model_md.metadata['validation_path']           = path_directory_validation
            self.model_md.metadata['valitation_steps_per_epoch']= steps_per_epoch_validation
        self.model_md.save()
        self.files_attached_md.save()
        
        return {"g_train":generator_train, "g_validation":generator_validation, "steps_per_epoch_train":steps_per_epoch_train, "steps_per_epoch_validation":steps_per_epoch_validation, "epochs":self.model_md.metadata['epoch_total']}