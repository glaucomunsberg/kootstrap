#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, time, sys
sys.path.append('../')

import keras.callbacks as callbacks
from system.Helper import Helper
from system.Logger import Logger
from system.Koopstrap import Koopstrap
from system.Metadata import Metadata

class KCallback(callbacks.Callback):
    
    _k          = None
    _helper     = None
    _logger     = None
    
    _model      = None
    _model_md   = None
    
    _each_epoch         = None
    _epoch              = None
    _start_time         = None
    _model_metadata_path    = None
    _output_model_weights   = None
    
    def __init__(self, model, model_metadata, logger=None):
        
        self._k         = Koopstrap()
        self._helper    = Helper()
        
        if logger == None:
            self._logger = Logger()
        else:
            self._logger    = logger
        
        self._model_md = model_metadata
        
        self._model                 = model
        self._each_epoch            = self._model_md.metadata['save_weights_to_each']
        self._epoch                 = 0
        
        self._output_model_weights  = self._k.path_model()+self._model_md.metadata['name']+"/weights/"
        
        if self._model_md.metadata['model_layers'] == []:
            for i, layer in enumerate(self._model.layers):
                self._model_md.metadata['model_layers'].append({'layer':i, 'layer_name':layer.name, 'layer_trainable':layer.trainable })
            self._model_md.save()
            
        self._logger.info('Callback: load with success')
        
    def on_epoch_begin(self, epoch, logs):
        self._start_time  = time.time()
        self._logger.info('Callback: Epoch {0} begin'.format(epoch))
        
        self._model_md.metadata['epoch_current'] = epoch
        self._model_md.save()
           
        if self._epoch == 0:
            file_name = self._output_model_weights+'weights_epoch_%03d.h5' % self._epoch
            self._logger.info('Callback: Saving weights at {0} file'.format(file_name))
            self._model.save_weights(file_name)
 			
    def on_epoch_end(self, epoch, logs):
        elapsed_time = time.time() - self._start_time
        self._epoch += 1
        self._logger.info('Callback: Epoch {0} end'.format(epoch))
        
        self._model_md.metadata['history_loss'].append(logs.get('loss'))
        self._model_md.metadata['history_acc'].append(logs.get('acc'))
        self._model_md.metadata['time_elapsed'].append(str(elapsed_time))
        self._model_md.save()
            
        if self._epoch % self._each_epoch == 0:
            
            file_name = self._output_model_weights+'weights_epoch_%03d.h5' % self._epoch
        
            self._logger.info('Callback: Saving weights at {0} file'.format(file_name))
            self._model.save_weights(file_name)
        
        if self._model_md.metadata['target_acc'] != -1.0 and logs.get('acc') >= self._model_md.metadata['target_acc']:
            self._logger.info('Callback: Stoping the training! Acc at {0} expected {1}'.format( logs.get('acc'), self._model_md.metadata['target_acc']))
            self._model.stop_training = True
        
        if self._model_md.metadata['target_loss'] != -1.0 and logs.get('loss') <= self._model_md.metadata['target_loss']:
            self._logger.info('Callback: Stoping the training! Loss at {0} expected {1}'.format( logs.get('loss'), self._model_md.metadata['target_loss']))
            self._model.stop_training = True
        
    def on_train_begin(self, logs={}):
        self._model_md.metadata['active'] = True
        self._model_md.metadata['begin_at'] = self._helper.getTimeNow()
        self._model_md.save()
            
    def on_train_end(self,logs={}):
        self._model_md.metadata['active'] = False
        self._model_md.metadata['end_at'] = self._helper.getTimeNow()
        self._model_md.save()