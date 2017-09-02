#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, sys, glob, random, os

sys.path.append('../')

from shutil import copyfile

from system.Koopstrap import Koopstrap
from system.Metadata import Metadata
from system.Logger import Logger
from system.Helper import Helper
from Dataset import Dataset
from Scissor import Scissor

class Compiler:
    
    _k          = None
    _logger     = None
    _helper     = None
    _args       = None
    
    dataset_name= None
    dataset_path= None
    dataset_md  = None
    
    subsets_path= None
    subset_name = None
    subset_path = None
    subset_md   = None
    
    subset_test_path    = None
    subset_train_path   = None
    list_of_classes     = None
    
    def __init__(self,args):
        
        self._k         = Koopstrap()
        self._logger    = Logger(app_name='Compiler')
        self._helper    = Helper()
        self._args      = args
        
        self.dataset_name   = Dataset.normalizeDatasetName(args.dataset_name)
        self.dataset_path   = self._k.path_dataset()+self.dataset_name+"/"
        self.dataset_md     = Metadata(self.dataset_path+"metadata.json")
        
        self.subsets_path   = self._k.path_dataset()+ self.dataset_name+"/subsets/"
        
        if args.subset_name != None:
            self.subset_name    = Dataset.normalizeDatasetName(args.subset_name)
        else:
            self.subset_name    = self.dataset_name+"_"+self._helper.getSerialNow()
        self._logger.info("Compiler: Subset name '{0}'".format(self.subset_name))
        
        self.subset_path    =  self.subsets_path+self.subset_name+"/"
            
        if not os.path.exists(self.subset_path):
            os.makedirs(self.subset_path)
            self.subset_md     = Metadata(self.subset_path+"metadata.json",True)
        else:
            self.subset_md     = Metadata(self.subset_path+"metadata.json")
            
        self.subset_train_path = self.subset_path+"train/"
        if not os.path.exists(self.subset_train_path):
            os.makedirs(self.subset_train_path)

        if self._args.validation_proportional_size > 0:
            self.subset_validation_path = self.subset_path+"validation/"
            if not os.path.exists(self.subset_validation_path):
                os.makedirs(self.subset_validation_path)
                
        if self._args.test_proportional_size > 0:
            self.subset_test_path = self.subset_path+"test/"
            if not os.path.exists(self.subset_test_path):
                os.makedirs(self.subset_test_path)
        else:
            self.subset_test_path = None
            
        if args.classes_load_file != None:
            self.list_of_classes = self._helper.filePathToList(args.classes_load_file)
        else:
            if args.classes == None:
                self.list_of_classes = [dI for dI in os.listdir(self.dataset_path+"classes/") if os.path.isdir(os.path.join(self.dataset_path+"classes/",dI))]
            else:
                self.list_of_classes = args.classes.split(",")
        self._logger.info("Compiler: Classes set {0}".format(self.list_of_classes))
        
        self.subset_md.metadata['name'] = self.subset_name
        self.subset_md.metadata['annotation'] = self._args.annotation
        self.subset_md.metadata['parental_serial'] = self.dataset_md.metadata['serial_identifier']
        self.subset_md.metadata['classes_order'] = self.dataset_md.metadata['classes_order']
        self.subset_md.metadata['parental_name'] = self.dataset_md.metadata['name']
        self.subset_md.metadata['serial_identifier'] = self._helper.getSerialNow()
        self.subset_md.metadata['created_at'] = self._helper.getTimeNow()
        self.subset_md.metadata['finished_at'] = ""
        self.subset_md.metadata['train_images'] = {}
        self.subset_md.metadata['validation_images'] = {}
        self.subset_md.metadata['test_images'] = {}
        self.subset_md.metadata['kootstrap_version'] = self._k.config['version']
        
        
        for class_name in self.list_of_classes:
            self.subset_md.metadata['train_images'][class_name] = []
            self.subset_md.metadata['validation_images'][class_name] = []
            self.subset_md.metadata['test_images'][class_name] = []
            
        if self._args.scissor == "yes":
            self._logger.info("Compiler: scissor '{0}'".format(self._args.scissor))
            self.subset_md.metadata['scissor']          = "yes"
            self.subset_md.metadata['scissor_rate']     = float(self._k.scissor['target_rate'])
            self.subset_md.metadata['scissor_min_with'] = int(self._k.scissor['target_min_width'])
            self.subset_md.metadata['scissor_min_height'] = int(self._k.scissor['target_min_height'])
        else:
            self._logger.info("Compiler: scissor '{0}'".format(self._args.scissor))
            self.subset_md.metadata['scissor'] = "no"
            
        if self._args.num_images == -1 and self._args.per_images == -1:
            self._logger.info("Compiler: slice type '{0}'".format("total"))
            self.subset_md.metadata['slicer_type'] = 'total'
        else:
            if self._args.per_images != -1:
                per_images = self._args.per_images
                if per_images > 100:
                    per_images = 100
                self._logger.info("Compiler: slice type '{0}'".format("percente"))
                self.subset_md.metadata['slicer_type'] = 'percente'
                self.subset_md.metadata['slicer_percente'] = self._args.per_images
            else:
                self._logger.info("Compiler: slice type '{0}'".format("partial"))
                self.subset_md.metadata['slicer_type'] = 'partial'
                self.subset_md.metadata['slicer_partional'] = self._args.num_images
                
        if self._k.config['file_order_randomly']:
            self.subset_md.metadata['file_order_randomly'] = 'yes'
        else:
            self.subset_md.metadata['file_order_randomly'] = 'no'
        self.subset_md.save()
        
    def start(self):
        
        for class_name in self.list_of_classes:
            
            print 'CLASS: ',class_name
            
            files_canditates_to_transfer        = glob.glob(self.dataset_path+"classes/"+class_name+"/*.*")
            num_of_files_canditates_to_transfer = len(files_canditates_to_transfer)
            
            path_train_class        = self.subset_train_path+class_name+"/"
            path_validation_class   = self.subset_validation_path+class_name+"/"
            path_test_class         = self.subset_test_path+class_name+"/"
            
            if not os.path.exists(path_train_class):
                os.makedirs(path_train_class)
            
            if self._args.validation_proportional_size > 0:
                if not os.path.exists(path_validation_class):
                    os.makedirs(path_validation_class)
                    
            if self._args.test_proportional_size > 0:
                if not os.path.exists(path_test_class):
                    os.makedirs(path_test_class)
                
            if self._k.config['file_order_randomly']:
                random.shuffle(files_canditates_to_transfer)
                
            # calculate the percent or total of images
            if self._args.num_images == -1 or self._args.per_images == 100:
                num_images = num_of_files_canditates_to_transfer
            elif self._args.per_images != -1:
                    per_images = self._args.per_images
                    if per_images > 100:
                        per_images = 100
                    num_images = (num_of_files_canditates_to_transfer*per_images)/100
            else:
                num_images = self._args.num_images
                if num_images > num_of_files_canditates_to_transfer:
                    num_images = num_of_files_canditates_to_transfer
                        
            # respect the global definition from slice information
            # after this split to train, validation and test sets
            files_canditates_to_transfer        = files_canditates_to_transfer[:num_images]
            num_of_files_canditates_to_transfer = len(files_canditates_to_transfer)
            
            files_to_transfer_train = []
            files_to_transfer_test = []
            files_to_transfer_validation = []
            # slice to train,validation and test group of images
                        
            if self._args.validation_proportional_size == 0:
                
                if self._args.train_proportional_size > 100:
                    raise ValueError('Train proportional not be great that 100%')
                    
                if self._args.train_proportional_size == 100:
                    self._logger.info("Compiler: Train set with 100%")
                    
                train_proportional_size = self._args.train_proportional_size
                
                train_size  = (num_of_files_canditates_to_transfer*train_proportional_size)/100
                test_size   = 100 - train_size
                
                files_to_transfer_train = files_canditates_to_transfer[:train_size]
                files_to_transfer_test  = files_canditates_to_transfer[train_size:]
                
                self.subset_md.metadata['train_proporcional_size'] = self._args.train_proportional_size
                self.subset_md.metadata['validation_proporcional_size'] = 0
                self.subset_md.metadata['test_proporcional_size'] = self._args.test_proportional_size
                self.subset_md.save()
                
            else:
                if self._args.train_proportional_size + self._args.validation_proportional_size + self._args.test_proportional_size > 100:
                    raise ValueError('train,validation and test sum more that 100%')
                else:
                    
                    train_proportional_size = self._args.train_proportional_size
                
                    train_size  = (num_of_files_canditates_to_transfer*train_proportional_size)/100
                    test_size   = 100 - train_size

                    files_to_transfer_train = files_canditates_to_transfer[:train_size]
                    files_to_split_validation_test  = files_canditates_to_transfer[train_size:]
                    
                    
                    validation_proporcional_split =(self._args.validation_proportional_size*100)/(self._args.validation_proportional_size+self._args.test_proportional_size)
                    
                    validation_size  = (len(files_to_split_validation_test)*validation_proporcional_split)/100
                    test_size   = 100 - validation_size
                    #print 'Validation proporcional',validation_size
                    #print 'Test       proporcional',test_size
                    
                    files_to_transfer_validation    = files_to_split_validation_test[:validation_size]
                    files_to_transfer_test          = files_to_split_validation_test[validation_size:]
                    #print 'Validation total',len(files_to_transfer_validation)
                    #print 'Test       total',len(files_to_transfer_test)
                    self.subset_md.metadata['train_proporcional_size'] = self._args.train_proportional_size
                    self.subset_md.metadata['validation_proporcional_size'] = self._args.validation_proportional_size
                    self.subset_md.metadata['test_proporcional_size'] = self._args.test_proportional_size
                    self.subset_md.save()
                    
            # of each group scissor or not the image and move
            for file_to_transfer in files_to_transfer_train:
                
                image_name = file_to_transfer.split('/')
                image_name = image_name[len(image_name)-1]
                image_name = image_name.split('.')
                image_name = image_name[0]
                image_path = file_to_transfer.replace(image_name,'')
                
                if self._args.scissor == "yes":
                    image = Scissor(file_to_transfer,self._logger)
                    image.cut_to_fit(path_train_class)
                    image.close()
                    if self._k.config['transfer_file_type'] != "copy":
                        os.remove(file_to_transfer)
                else:
                    if self._k.config['transfer_file_type'] == "copy":
                        self._logger.info("Compiler: Copy file '{0}'".format(image_name))
                        shutil.copyfile(file_to_transfer+file_name, path_train_class+image_name)
                    else:
                        self._logger.info("Compiler: Move file '{0}'".format(image_name))
                        shutil.move(file_to_transfer, path_train_class+image_name)
                        
                self.subset_md.metadata['train_images'][class_name].append(image_name)
                self._logger.info("Compiler: send {0} to train/{1}/".format(image_name,class_name))
                
            for file_to_transfer in files_to_transfer_test:
                
                
                image_name = file_to_transfer.split('/')
                image_name = image_name[len(image_name)-1]
                image_name = image_name.split('.')
                image_name = image_name[0]
                image_path = file_to_transfer.replace(image_name,'')
                
                if self._args.scissor == "yes":
                    image = Scissor(file_to_transfer,self._logger)
                    image.cut_to_fit(path_test_class)
                    image.close()
                    if self._k.config['transfer_file_type'] != "copy":
                        os.remove(file_to_transfer)
                else:
                    if self._k.config['transfer_file_type'] == "copy":
                        self._logger.info("Compiler: Copy file '{0}'".format(image_name))
                        shutil.copyfile(file_to_transfer+file_name, path_test_class+image_name)
                    else:
                        self._logger.info("Compiler: Move file '{0}'".format(image_name))
                        shutil.move(file_to_transfer, path_test_class+image_name)
                
                self.subset_md.metadata['test_images'][class_name].append(image_name)
                self._logger.info("Compiler: send {0} to test/{1}/".format(image_name,class_name))
                
            for file_to_transfer in files_to_transfer_validation:
                
                image_name = file_to_transfer.split('/')
                image_name = image_name[len(image_name)-1]
                image_name = image_name.split('.')
                image_name = image_name[0]
                image_path = file_to_transfer.replace(image_name,'')
                
                if self._args.scissor == "yes":
                    image = Scissor(file_to_transfer,self._logger)
                    image.cut_to_fit(path_validation_class)
                    image.close()
                    if self._k.config['transfer_file_type'] != "copy":
                        os.remove(file_to_transfer)
                else:
                    if self._k.config['transfer_file_type'] == "copy":
                        self._logger.info("Compiler: Copy file '{0}'".format(image_name))
                        shutil.copyfile(file_to_transfer+file_name, path_validation_class+image_name)
                    else:
                        self._logger.info("Compiler: Move file '{0}'".format(image_name))
                        shutil.move(file_to_transfer, path_validation_class+image_name)
                        
                self.subset_md.metadata['validation_images'][class_name].append(image_name)
                self._logger.info("Compiler: send {0} to validation/{1}/".format(image_name,class_name))
        
        self.subset_md.metadata['finished_at'] = self._helper.getTimeNow()
        self.subset_md.save()
        
class Seeder:
    
    _k              = None
    _helper         = None
    _logger         = None
    
    classes_images  = None
    path_subsets    = None
    path_dataset    = None
    subsets_list    = None
    
    def __init__(self,path_dataset,classes_images,logger=None):
        
        if logger == None:
            self._logger = Logger('Seeder')
        else:
            self._logger = logger
            
        self._k = Koopstrap()
        
        self.classes_images = classes_images
        
        self.path_subsets = path_dataset+"subsets/"
        self.path_classes = path_dataset+"classes/"
        
        self.subsets_list = [dI for dI in os.listdir(self.path_subsets) if os.path.isdir(os.path.join(self.path_subsets,dI))]
        
    def seed(self):
        
        for class_name,values in self.classes_images.iteritems():
            list_images_candidates = []
            for value in values:
                list_images_candidates.append(value['name'])
                
                
            list(list_images_candidates)
            for subset_name in self.subsets_list:
                
                subset_md               = Metadata(self.path_subsets+subset_name+"/metadata.json")
                
                subset_train_path       = self.path_subsets+subset_name+"/train/"
                subset_validation_path  = self.path_subsets+subset_name+"/validation/"
                subset_test_path        = self.path_subsets+subset_name+"/test/"
                
                path_train_class        = subset_train_path+class_name+"/"
                path_validation_class   = subset_validation_path+class_name+"/"
                path_test_class         = subset_test_path+class_name+"/"
                
                if not os.path.exists(path_train_class):
                    os.makedirs(path_train_class)

                if subset_md.metadata['validation_proporcional_size'] > 0:
                    if not os.path.exists(path_validation_class):
                        os.makedirs(path_validation_class)

                if subset_md.metadata['test_proporcional_size'] > 0:
                    if not os.path.exists(path_test_class):
                        os.makedirs(path_test_class)
                
                files_canditates_to_transfer        = list(list_images_candidates)
                num_of_files_canditates_to_transfer = len(files_canditates_to_transfer)
                files_to_transfer_train             = []
                files_to_transfer_test              = []
                files_to_transfer_validation        = []
                
                # respect the global definition from slice information
                # after this split to train, validation and test sets
                if subset_md.metadata['slicer_type'] == "total":
                    num_images = len(files_canditates_to_transfer)
                elif subset_md.metadata['slicer_type'] == "partial":
                    num_images = self.subset_md.metadata['slicer_partial']
                    if num_images > num_of_files_canditates_to_transfer:
                        num_images = num_of_files_canditates_to_transfer
                else:
                    # percente
                    per_images = subset_md.metadata['slicer_percente']
                    if per_images > 100:
                        per_images = 100
                    num_images = (len(files_canditates_to_transfer)*per_images)/100
                
                if subset_md.metadata['file_order_randomly'] == "yes":
                    random.shuffle(files_canditates_to_transfer)
                    
                files_canditates_to_transfer = files_canditates_to_transfer[:num_images]
                
                if subset_md.metadata['train_proporcional_size'] == 100:
                    files_to_transfer_train = files_canditates_to_transfer
                else:
                    train_proportional_size = subset_md.metadata['train_proporcional_size']
                    test_proportional_size = subset_md.metadata['test_proporcional_size']
                    validation_proportional_size = subset_md.metadata['validation_proporcional_size']
                    
                    train_size  = (num_of_files_canditates_to_transfer*train_proportional_size)/100
                    test_size   = (num_of_files_canditates_to_transfer*test_proportional_size)/100
                    validation_size   = (num_of_files_canditates_to_transfer*validation_proportional_size)/100
                    
                    files_to_transfer_train         = files_canditates_to_transfer[:train_size]
                    
                    files_to_split_validation_test  = files_canditates_to_transfer[train_size:]
                    files_to_transfer_validation    = files_to_split_validation_test[:validation_size]
                    files_to_transfer_test          = files_to_split_validation_test[validation_size:]
                    
                    #print 'To total', len(files_canditates_to_transfer)
                    #print 'To Train', len(files_to_transfer_train)
                    #print 'To Valid', len(files_to_transfer_validation)
                    #print 'To Test ', len(files_to_transfer_test)
                    
                    for file_to_transfer in files_to_transfer_train:
                        image_path = self.path_classes+class_name+"/"
                        image_name = file_to_transfer
                        
                        if subset_md.metadata['scissor'] == "yes":
                            image = Scissor(image_path+image_name,self._logger)
                            image.cut_to_fit(path_train_class)
                            image.close()
                            if self._k.config['transfer_file_type'] != "copy":
                                os.remove(file_to_transfer)
                        else:
                            if self._k.config['transfer_file_type'] == "copy":
                                self._logger.info("Compiler: Copy file '{0}'".format(image_name))
                                shutil.copyfile(file_to_transfer+file_name, path_train_class+image_name)
                            else:
                                self._logger.info("Compiler: Move file '{0}'".format(image_name))
                                shutil.move(file_to_transfer, path_train_class+image_name)
                        subset_md.metadata['train_images'][class_name].append(image_name)
                        self._logger.info("Compiler: send {0} to train/{1}/".format(image_name,class_name))
                        
                    for file_to_transfer in files_to_transfer_validation:
                        image_path = self.path_classes+class_name+"/"
                        image_name = file_to_transfer
                        
                        if subset_md.metadata['scissor'] == "yes":
                            image = Scissor(image_path+image_name,self._logger)
                            image.cut_to_fit(path_validation_class)
                            image.close()
                            if self._k.config['transfer_file_type'] != "copy":
                                os.remove(file_to_transfer)
                        else:
                            if self._k.config['transfer_file_type'] == "copy":
                                self._logger.info("Compiler: Copy file '{0}'".format(image_name))
                                shutil.copyfile(file_to_transfer+file_name, path_validation_class+image_name)
                            else:
                                self._logger.info("Compiler: Move file '{0}'".format(image_name))
                                shutil.move(file_to_transfer, path_validation_class+image_name)
                        subset_md.metadata['validation_images'][class_name].append(image_name)
                        self._logger.info("Compiler: send {0} to train/{1}/".format(image_name,class_name))
                        
                    for file_to_transfer in files_to_transfer_test:
                        image_path = self.path_classes+class_name+"/"
                        image_name = file_to_transfer
                        
                        if subset_md.metadata['scissor'] == "yes":
                            image = Scissor(image_path+image_name,self._logger)
                            image.cut_to_fit(path_test_class)
                            image.close()
                            if self._k.config['transfer_file_type'] != "copy":
                                os.remove(file_to_transfer)
                        else:
                            if self._k.config['transfer_file_type'] == "copy":
                                self._logger.info("Compiler: Copy file '{0}'".format(image_name))
                                shutil.copyfile(file_to_transfer+file_name, path_test_class+image_name)
                            else:
                                self._logger.info("Compiler: Move file '{0}'".format(image_name))
                                shutil.move(file_to_transfer, path_test_class+image_name)
                        subset_md.metadata['test_images'][class_name].append(image_name)
                        self._logger.info("Compiler: send {0} to train/{1}/".format(image_name,class_name))
                        
                subset_md.save()