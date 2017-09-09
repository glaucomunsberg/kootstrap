#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, json, sys
sys.path.append('../')

from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.models import Model, model_from_json
from keras.optimizers import SGD
from system.Helper import Helper
from system.Logger import Logger
from Callbacks import KCallback
from Mananger import Mananger

class Trainer:

    _helper             = None
    _logger             = None
    
    mananger    = None
    model       = None
    
    def __init__(self, args):

        self._helper    = Helper()
        self._logger    = Logger('Trainer')
        self.mananger    = Mananger(args,self._logger)

        self.model  = self.mananger.getModel()
    
        self.mananger.printModel(self.model)

    def start(self):

        # frozen the layout after the last
        for layer in self.model.layers[:len(self.model.layers)-2]:
            self._logger.info("Trainer: Layer {0} is not trainable".format(layer.name))
            layer.trainable = False

        # traing the last layer
        for layer in self.model.layers[len(self.model.layers)-2:]:
            self._logger.info("Trainer: Layer {0} is trainable".format(layer.name))
            layer.trainable = True

        self._logger.info('Trainer: compile the model')
        self.model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy', metrics=['accuracy'])

        self._logger.info('Trainer: fit generator')
        
        k_generators = self.mananger.configFitGenerator()
        
        k_callbacks = self.mananger.getCallbacks()
        
        self.model.fit_generator(k_generators["g_train"], k_generators["steps_per_epoch_train"], epochs= k_generators["epochs"], verbose=2, callbacks= self.mananger.getCallbacks(), validation_data= k_generators["g_validation"], validation_steps=k_generators["steps_per_epoch_validation"])
        
        self.mananger.save(self.model)