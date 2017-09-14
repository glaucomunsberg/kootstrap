#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob, os, random, argparse, sys,shutil
sys.path.append('../')

from system.Kootstrap import Kootstrap
from system.Logger import Logger

class Transfer:
    
    _k              = None
    _logger         = None
    
    images_folder   = None
    images_destity  = None
    number_of_images= None
    file_order_randomly   = None
    
    def __init__(self, args):
        
        self._k                 = Kootstrap()
        self._logger            = Logger('Tools')
        
        self.images_folder      = args.path_origin
        self.images_destity     = args.path_destiny
        
        if self.images_destity[-1:] != "/":
            self.images_destity+= "/"
        
        self.number_of_images   = args.max_files_by_class
        if self.number_of_images == -1:
            self.number_of_images = float('inf')
        
        self.file_order_randomly = self._k.config['file_order_randomly']
        
        if args.copy_way == None:
            self.copy_way           = self._k.config['transfer_file_type']
        else:
            if args.copy_way == "copy":
                self.copy_way = True
            else:
                self.copy_way = False
                
        self._logger.info("Transfer: --path_origin is '{0}'".format(args.path_origin))
        self._logger.info("Transfer: --path_destiny is '{0}'".format(args.path_destiny))
        self._logger.info("Transfer: --number_of_images is '{0}'".format(self.number_of_images))
        self._logger.info("Transfer: --copy_way is '{0}'".format(self.copy_way))
        
    def start(self):
        moved = 0
        if not os.path.exists(self.images_folder):
            print 'Source',self.images_folder,'not exist!'
            return False
        
        if not os.path.exists(self.images_destity):
            print 'Destity',self.images_destity,'was created'
            os.makedirs(self.images_destity)
        
        #os.chdir(self.images_folder)
        files_to_transfer = glob.glob(self.images_folder+"*.*")
        
        if self.file_order_randomly == True:
            random.shuffle(files_to_transfer)
            
        files_names = []
        for file in files_to_transfer:
            files_names.append(file.split("/")[-1:][0])
        
        for file_name in files_names:
            if os.path.isfile(os.path.join(self.images_folder,file_name)) and file_name != ".DS_Store" and os.stat(self.images_folder+file_name).st_size!=0:
                if moved < self.number_of_images:
                    
                    self._logger.info("Transfer: file {0} - {1} moved".format(moved,file_name))
                    print 'file ',moved, 'name', file_name
                    
                    if self.copy_way:
                        shutil.copyfile(self.images_folder+file_name, self.images_destity+file_name)
                    else:
                        shutil.move(self.images_folder+file_name, self.images_destity+file_name)
                    moved+=1
                    
        self._logger.info("Transfer: Total {0} images moved".format(moved))