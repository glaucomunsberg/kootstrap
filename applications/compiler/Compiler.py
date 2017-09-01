#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, sys, glob, random, os

sys.path.append('../')

from shutil import copyfile

from system.Koopstrap import Koopstrap
from system.Metadata import Metadata
from system.Logger import Logger
from system.Helper import Helper
from crawler.Dataset import Dataset
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

        self.subset_path    =  self.subsets_path+self.subset_name+"/"
            
        if not os.path.exists(self.subset_path):
            os.makedirs(self.subset_path)
            self.subset_md     = Metadata(self.subset_path+"metadata.json",True)
        else:
            self.subset_md     = Metadata(self.subset_path+"metadata.json")
            
        self.subset_train_path = self.subset_path+"train/"
        if not os.path.exists(self.subset_train_path):
            os.makedirs(self.subset_train_path)

        if args.test_set == "yes":
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
        
        self.subset_md.metadata['name'] = self.subset_name
        self.subset_md.metadata['annotation'] = self._args.annotation
        self.subset_md.metadata['created_at'] = self._helper.getTimeNow()
        
        if self._args.test_set == "yes":
            self.subset_md.metadata['test_set'] = "yes"
        else:
            self.subset_md.metadata['test_set'] = "no"
            
        if self._args.scissor == "yes":
            self.subset_md.metadata['scissor']          = "yes"
            self.subset_md.metadata['scissor_rate']     = float(self._k.scissor['target_rate'])
            self.subset_md.metadata['scissor_min_with'] = int(self._k.scissor['target_min_width'])
            self.subset_md.metadata['scissor_min_height'] = int(self._k.scissor['target_min_height'])
        else:
            self.subset_md.metadata['scissor'] = "no"
            
        if self._args.num_images == -1 and self._args.per_images == -1:
                self.subset_md.metadata['slicer_type'] = 'total'
                self.subset_md.metadata['slicer_total'] = num_images
        else:
            if self._args.per_images != -1:
                per_images = self._args.per_images
                if per_images > 100:
                    per_images = 100
                self.subset_md.metadata['slicer_type'] = 'percente'
                self.subset_md.metadata['slicer_per'] = str(per_images)+"%"
            else:
                self.subset_md.metadata['slicer_type'] = 'partial'
                
        if self._k.config['file_order_randomly']:
            self.subset_md.metadata['file_order_randomly'] = 'yes'
        else:
            self.subset_md.metadata['slicer_type'] = 'no'
        self.subset_md.save()
        
    def start(self):
        
        for class_name in self.list_of_classes:
            
            print 'CLASS: ',class_name
            
            files_canditates_to_transfer        = glob.glob(self.dataset_path+"classes/"+class_name+"/*.*")
            num_of_files_canditates_to_transfer = len(files_canditates_to_transfer)
            
            path_train_class    = self.subset_train_path+class_name+"/"
            path_test_class     = self.subset_test_path+class_name+"/"
            
            if not os.path.exists(path_test_class):
                os.makedirs(path_test_class)
                
            if not os.path.exists(path_train_class):
                os.makedirs(path_train_class)
            
            print 'total canditates', num_of_files_canditates_to_transfer
                
            if self._k.config['file_order_randomly']:
                random.shuffle(files_canditates_to_transfer)
                
            # calculate the percent or total of images
            if self._args.num_images == -1 and self._args.per_images == -1:
                num_images = num_of_files_canditates_to_transfer
            else:
                if self._args.per_images != -1:
                    per_images = self._args.per_images
                    if per_images > 100:
                        per_images = 100
                    num_images = (num_of_files_canditates_to_transfer*per_images)/100
                else:
                    num_images = self._args.num_images
                    if num_images > num_of_files_canditates_to_transfer:
                        num_images = num_of_files_canditates_to_transfer
                        
            #compile the list to send to train or test set
            files_canditates_to_transfer        = files_canditates_to_transfer[:num_images]
            num_of_files_canditates_to_transfer = len(files_canditates_to_transfer)
            
            files_to_transfer_train = []
            files_to_transfer_test = []
            
            # slice to test and train group of images
            if self._args.test_set == "yes":
                
                if self._args.train_proportional_size > 100:
                    train_proportional_size = 100
                else:
                    train_proportional_size = self._args.train_proportional_size
                    
                train_size  = (num_of_files_canditates_to_transfer*train_proportional_size)/100
                test_size   = 100 - train_size
                
                files_to_transfer_train = files_canditates_to_transfer[:train_size]
                files_to_transfer_test  = files_canditates_to_transfer[train_size:]
                
            else:
                files_to_transfer_train = files_canditates_to_transfer
            
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
                        shutil.copyfile(file_to_transfer+file_name, path_train_class+image_name)
                    else:
                        shutil.move(file_to_transfer, path_train_class+image_name)
                
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
                        shutil.copyfile(file_to_transfer+file_name, path_test_class+image_name)
                    else:
                        shutil.move(file_to_transfer, path_test_class+image_name)