import argparse, json, sys, os
import numpy as np
sys.path.append('../')

from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input, decode_predictions
from keras.preprocessing import image
from system.Helper import Helper
from system.Logger import Logger
from system.Koopstrap import Koopstrap
from Mananger import Mananger

class Tester:
    
    _k              = None
    _helper         = None
    _logger         = None
    _path_model     = None
    _path_dataset   = None
    
    model           = None
    mananger        = None
    
    total_files     = None
    current_file    = None
    def __init__(self,args):
        
        self._k         = Koopstrap()
        self._helper    = Helper()
        self._logger    = Logger('Tester')
        
        self.mananger   = Mananger(args,self._logger)    
        self.file_predictions = self.mananger.test_predictions_csv
        
    
    def start(self):
        
        
        self.model = self.mananger.getModelWithWeights()
        
        self.mananger.test_md.metadata['start_at']     = self._helper.getTimeNow()
        self.mananger.test_md.save()
        
        
        self.total_files = 0
        self.current_file= 0
        # calculate number of images
        for class_name in self.mananger.classes_order:
            if self.mananger.dataset_set_type == 'subset':
                path_images_by_class = self.mananger.path_load_set+class_name+"/"
            else:
                path_images_by_class = self.mananger.path_load_set+"classes/"+class_name+"/"
            fist_of_files = [f for f in os.listdir(path_images_by_class) if os.path.isfile(path_images_by_class+f)]
            self.total_files+=len(fist_of_files)
            
        # of each class and each image predict the class and save at file!
        for class_name in self.mananger.classes_order:
            if self.mananger.dataset_set_type == 'subset':
                path_images_by_class = self.mananger.path_load_set+class_name+"/"
            else:
                path_images_by_class = self.mananger.path_load_set+"classes/"+class_name+"/"
                
            #print 'class',path_images_by_class
            
            fist_of_files = [f for f in os.listdir(path_images_by_class) if os.path.isfile(path_images_by_class+f)]
            for file_name in fist_of_files:
                #print 'Class name: ',class_name,' and file: ',file_name
                file_path = path_images_by_class+f
                
                if file_name != ".DS_Store" and os.stat(file_path).st_size!=0:
                    img = image.load_img(file_path, target_size=(self.mananger.model_md.metadata['target_size'], self.mananger.model_md.metadata['target_size']))
                    x = image.img_to_array(img)
                    x = np.expand_dims(x, axis=0)
                    x = preprocess_input(x)
                    self._logger.info('Tester: Appending image {0} {2} from {1}'.format( file_name, self.total_files, self.current_file))
                    predictions = self.model.predict(x)
                    for probabilities in predictions:
                        row_output    = class_name+";"+file_name+";"

                        for probability in probabilities:
                            row_output += str(probability)+";"

                    self.file_predictions.write(row_output+os.linesep)
                else:
                    self._logger.info("Tester: Can't apppend image {0} to session".format(file_name))
                self.current_file += 1
                
        self.mananger.test_md.metadata['end_at']     = self._helper.getTimeNow()
        self.mananger.test_md.save()