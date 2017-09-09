#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Generator:

    imageDateGeneratorValidation   = None
    imageDateGeneratorTrain        = None

    _k                      = None
    _target_size            = None   
    _batch_size             = None   

    _path_directory         = None 
    _path_file_classes      = None 
    _path_classes_name      = []

    def __init__(self,metadata_model):

        self._path_directory    = args.path_directory       # "/home/glauco/data/ImageNetGraffitiWithoutImages/"
        self._path_file_classes = args.path_file_classes    # "../helpers/extractor/data/synset_words.txt"
        self._target_size       = args.target_size          # size of pic (w x h) 244
        self._batch_size        = args.batch_size           # 128
        
        with open(self._path_file_classes) as file:
            lines = file.readlines()
            for line in lines:
                self._path_classes_name.append(line[:9])
        self._imageDateimage = image.ImageDataGenerator(rescale=0).flow_from_directory(self._path_directory, target_size=(self._target_size, self._target_size), batch_size= self._batch_size, class_mode='categorical', shuffle=True, classes=self._path_classes_name)

    def getTrainGenerator(self):
        return self.imageDateGeneratorTrain
    
    def getValidationGenerator(self):
        return self.imageDateGeneratorValidation