#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math, sys, wand
sys.path.append('../')

from wand.image import Image
from wand.display import display

from system.Logger import Logger
from system.Kootstrap import Kootstrap

class Scissor:
    
    _logger = None
    
    original_image_url  = ""
    original_width      = 0
    original_height     = 0
    image_name          = ""
    image               = None
    
    width               = 0
    height              = 0
    window_width        = 0
    window_height       = 0
    manipulated         = False
    
    def __init__(self,image_url="",logger=None):
        
        self._k         = Kootstrap()
        if logger == None:
            self._logger    = Logger()
        else:
            self._logger    = logger
        
        self.original_image_url = image_url
        
        self.image_name = self.original_image_url.split('/')
        self.image_name = self.image_name[len(self.image_name)-1]
        self.image_name = self.image_name.split('.')
        self.image_name = self.image_name[0]
        
        with Image(filename=self.original_image_url) as img:
            
            self.image          = img.clone()
            
            self.width          = int(img.size[0])
            self.height         = int(img.size[1])
            self.window_width   = int(img.size[0])
            self.window_height  = int(img.size[1])
            self.original_width = int(img.size[0])
            self.original_height= int(img.size[1])

    def cut_to_fit(self, destiny_path=None):
        
        max_width   = int(self._k.scissor['target_max_width'])
        max_height  = int(self._k.scissor['target_max_height'])
        rate        = float(self._k.scissor['target_rate'])
        min_width   = int(self._k.scissor['target_min_width'])
        min_height  = int(self._k.scissor['target_min_height'])
        
        new_width   = 0
        new_height  = 0
        need_cut    = False
        need_rate   = False
    
        # First cut the windows based on rate
        if rate < 1.0:
            self.window_width   = int(self.width*rate)
            self.window_height  = int(self.height*rate)
            self.width          = self.window_width
            self.height         = self.window_height
            self.image.crop(width=self.window_width, height=self.window_height, gravity='center')
            #print 'Cut and rate',self.width,'x',self.height

        # Calculate if the width is greater than max width value
        if max_width != None and self.width > max_width:
            # cut the width first
            new_width           = max_width
            new_height          = int(math.ceil((self.height*max_width)/self.width))
            if new_height >= max_height:
                need_cut            = True
                self.manipulated    = True
                self.width          = new_width
                self.height         = new_height
                #print 'Need cut by max_width',new_width,'x',new_height

        # Calculate if the width is greater than max width value
        if max_height != None and self.height > max_height:
        #   # cut the height if necessary
            new_height          = max_height
            new_width           = int(math.ceil((self.width*max_height)/self.height))
            if new_width >= max_width:
                need_cut            = True
                self.manipulated    = True
                self.width          = new_width
                self.height         = new_height
                #print 'Need cut by max_height',new_width,'x',new_height

        # Save the file
        if need_cut:
            self.image.resize(self.width,self.height)
            #print 'Need resize ',self.width,'x',self.height

        self.image.crop(width=max_width, height=max_height, gravity='center')
        if need_cut or need_rate:
            self._logger.info('Scissor: created image {0}-{1}x{2}_resized.{3}'.format( self.image_name, self.image.width, self.image.height, self.image.format.lower()))
            self.image.save(filename='{0}{1}-{2}x{3}_resized.{4}'.format(destiny_path, self.image_name, self.image.width, self.image.height, self.image.format.lower()))
        elif max_height != None and max_width != None and max_height >= self.height and max_width >= self.width:
            self._logger.info('Scissor: created image {0}-{1}x{2}_original.{3}'.format( self.image_name, self.image.width, self.image.height, self.image.format.lower()))
            self.image.save(filename='{0}{1}-{2}x{3}_original.{4}'.format(destiny_path, self.image_name, self.image.width, self.image.height, self.image.format.lower()))
        else:
            self._logger.info('Scissor: not create new image {0}-{1}x{2}.{3} on repository'.format( self.image_name, self.image.width, self.image.height, self.image.format.lower()))
        
    def close(self):
        self.image.close()
        self._logger = None