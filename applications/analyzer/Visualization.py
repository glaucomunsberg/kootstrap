import matplotlib
matplotlib.use('Agg') # fixing -X screen
import matplotlib.pyplot as plt

import argparse, sys, os
sys.path.append('../')

from keras import activations
from keras.applications import VGG16
from keras.models import model_from_json
from vis.visualization import visualize_cam
from vis.utils import utils

from trainer.Model import Model
from system.Kootstrap import Kootstrap
from system.Metadata import Metadata
from system.Helper import Helper
from system.Logger import Logger

class Visualization:
    
    _k                  = None
    _helper             = None
    _logger             = None
    
    path_images         = None
    path_destiny        = None
    path_model_json     = None
    path_model_weights  = None
    path_test_model_visualization_file  = None
    
    serial_number   = None
    
    show_both       = None
    
    images_list     = None
    
    model           = None
    
    def __init__(self,args,logger=None):
        
        if logger == None:
            self._logger = Logger('Visualization')
        else:
            self._logger = logger
        
        self._helper    = Helper()
        self._k         = Kootstrap()
        
        self.path_images    = args.files.split(",")
        self.title          = args.title
        self.modifiers      = args.modifier.split(",")
        self.serial_number  = self._helper.getSerialNow()
        
        if args.show_both == "yes":
            self.show_both = True
        else:
            self.show_both = False
            
        self.images_list    = []
        
        # select the model by name
        if args.model_name == None:
            raise ValueError('arg --model_name need by setted')
        else:
            self.model_name = Model.normalizeModelName(args.model_name)
            self.path_model = Model.pathFromModelName(self.model_name)
            
        if self.model_name == None:
            raise ValueError('arg --model_name is not a valid url or name')
            
        if self.path_model == None:
            raise ValueError('arg --model_name is not a valid model path')
        
        self.model_md           = Metadata(self.path_model+"metadata.json")
        self.path_model_json    = self.path_model+"model.json"
        
        self.path_destiny       = self._k.path_test()+self.model_name+"/"+self.serial_number+"_visualization/"
    
        json_file = open(self.path_model_json, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        
        if args.epoch == -1:
            self.path_model_weights = self.path_model+"weights/weights.h5"
        else:
            self.path_model_weights = self.path_model+"weights/weights_epoch_%03d.h5" % self.epoch
        
        self.model.load_weights(self.path_model_weights)
        
        self.class_position = self.model_md.metadata['classes'].index(args.class_name)
            
        for image_path in self.path_images:
            self.images_list.append(utils.load_img(image_path, target_size=(self.model_md.metadata['target_size'], self.model_md.metadata['target_size'])))
        
    def start(self):
        
        if not os.path.exists(self.path_destiny):
            os.makedirs(self.path_destiny)
            
        
        # Utility to search for layer index by name. 
        # Alternatively we can specify this as -1 since it corresponds to the last layer.
        layer_idx = utils.find_layer_idx(self.model, 'predictions')
        self.model.layers[layer_idx].activation = activations.linear
        self.model = utils.apply_modifications(self.model)
        
        for modifier in self.modifiers:
            
            fig = plt.figure()
            if self.show_both:
                plt.subplots(1, len(self.images_list), squeeze=False)
            else:
                plt.subplots(1, 1, squeeze=False)
            plt.suptitle(self.title if modifier is None else self.title+" "+modifier)
            
            if modifier == 'None' or modifier == 'none':
                modifier = None
            
            for i, img in enumerate(self.images_list):    
                # 20 is the imagenet index corresponding to `ouzel`
                heatmap = visualize_cam(self.model, layer_idx, filter_indices=self.class_position, 
                                        seed_input=img, backprop_modifier=modifier)
                if self.show_both:
                    plt.subplot(1,2,i+1)
                    plt.imshow(img, interpolation='none')

                    plt.subplot(1,2,i+2)
                    plt.imshow(img, interpolation='none')
                    plt.imshow(heatmap, interpolation='none', alpha=0.7)
                else:
                    plt.imshow(img, interpolation='none')
                    plt.imshow(heatmap, interpolation='none', alpha=0.7)
        
                if modifier == None:
                    modifier = ""
                file_name_out = self.path_images[i].split('/')
                file_name_out = file_name_out[len(file_name_out)-1:][0]
                file_name_out_png = self.path_destiny+"class_"+str(self.class_position)+"_"+modifier+"_"+file_name_out
                print 'save at',file_name_out_png
                plt.savefig(file_name_out_png)
                
                plt.show()