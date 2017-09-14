import os, sys, glob
sys.path.append('../')

from system.Kootstrap import Kootstrap
from system.Metadata import Metadata
from system.Logger import Logger
from system.Helper import Helper
from maker.Dataset import Dataset

class FixMetadata:
    
    _k                  = None
    _logger             = None
    _helper             = None
    
    path_folder_origin  = None
    remove_previous     = None
    create_set          = None
    set_md              = None
    
    def __init__(self,args):
        
        self._helper    = Helper()
        self._logger    = Logger('Tools')
        self._k         = Kootstrap()
        
        self.path_folder_origin = args.path_origin
        
        sub_folders_origin = [dI for dI in os.listdir(self.path_folder_origin) if os.path.isdir(os.path.join(self.path_folder_origin,dI))]
        
        if "classes" in sub_folders_origin and "subsets" in sub_folders_origin:
            
            if os.path.isfile(self.path_folder_origin+"metadata.json"):
                value      = raw_input("We find the metadata.json file. Do you want update informations and images references? y/n")
                if value.upper() != "Y":
                    value      = raw_input("We find the metadata.json file. Do you erase the informations and recompile? y/n")
                    if value.upper() != "Y":
                        print "OK bye"
                        return ""
                    else:
                        create_set      = False
                        remove_previous = True
                else:
                    create_set      = False
                    remove_previous = False
            else:
                create_set      = True
                remove_previous = False
            if remove_previous:
                os.remove(self.path_folder_origin+"metadata.json")
                self.set_md = Metadata(self.path_folder_origin+"metadata.json",True)
            else:
                self.set_md = Metadata(self.path_folder_origin+"metadata.json")
            
            if create_set:
                self.set_md = Metadata(self.path_folder_origin+"metadata.json",True)
            
            if create_set or remove_previous:
                bits_path = self.path_folder_origin.split("/")
                if bits_path[-1:][0] == "":
                    del bits_path[len(bits_path)-1]
                name = bits_path[-1:][0]
                self.set_md.metadata['name']                = name
                self.set_md.metadata['serial_identifier']   = self._helper.getSerialNow()
                self.set_md.metadata['created_at']          = self._helper.getTimeNow()
                self.set_md.metadata['classes']             = {}
                self.set_md.metadata['classes_order']       = []
                self.set_md.metadata['annotation']          = ""
            else:
                self.set_md.metadata['classes']         = {}
                self.set_md.metadata['classes_order']   = []
            self.set_md.save()
            
            path_folder_origin_classes = self.path_folder_origin+"classes/"
            classes = [dI for dI in os.listdir(path_folder_origin_classes) if os.path.isdir(os.path.join(path_folder_origin_classes,dI))]
            print 'CLASSES',classes
            self.set_md.metadata['classes_order'] = classes
            for class_name in classes:
                self.set_md.metadata['classes'][class_name] = {}
                self.set_md.metadata['classes'][class_name]['num_images'] = 0
                self.set_md.metadata['classes'][class_name]['images'] = []
                self.set_md.save()
                
                files_to_transfer = glob.glob(path_folder_origin_classes+class_name+"/*.*")
                
                files_names = []
                #print "FILES to TRASNFER",files_to_transfer
                for file in files_to_transfer:
                    files_names.append(file.split("/")[-1:][0])
                    
                for file_name in files_names:
                    if os.path.isfile(os.path.join(path_folder_origin_classes+class_name+"/",file_name)) and file_name != ".DS_Store" and os.stat(path_folder_origin_classes+class_name+"/"+file_name ).st_size!=0:
                        self.set_md.metadata['classes'][class_name]['num_images'] += 1
                        self.set_md.metadata['classes'][class_name]['images'].append(file_name)
                    else:
                        print "NOT FILE"
            self.set_md.save()
            # is a dataset
        elif "train" in sub_folders_origin:
            if os.path.isfile(self.path_folder_origin+"metadata.json"):
                value      = raw_input("We find the metadata.json file. Do you want update informations and images references? y/n")
                if value.upper() != "Y":
                    value      = raw_input("We find the metadata.json file. Do you erase the informations and recompile? y/n")
                    if value.upper() != "Y":
                        print "OK bye"
                        return ""
                    else:
                        create_set      = False
                        remove_previous = True
                else:
                    create_set      = False
                    remove_previous = False
            else:
                create_set      = True
                remove_previous = False
            if remove_previous:
                os.remove(self.path_folder_origin+"metadata.json")
                self.set_md = Metadata(self.path_folder_origin+"metadata.json",True)
            else:
                self.set_md = Metadata(self.path_folder_origin+"metadata.json")
            
            if create_set:
                self.set_md = Metadata(self.path_folder_origin+"metadata.json",True)
            
            try:
                self.dataset_md = Metadata(self.path_folder_origin+"../../metadata.json")
            except:
                print "The subset is inside of a invalid dataset!"
                return ""
            
            if create_set or remove_previous:
                bits_path = self.path_folder_origin.split("/")
                if bits_path[-1:][0] == "":
                    del bits_path[len(bits_path)-1]
                name = bits_path[-1:][0]
                self.set_md.metadata['name']                = name
                self.set_md.metadata['annotation']          = ""
                self.set_md.metadata['parental_serial']     = self.dataset_md.metadata['serial_identifier']
                self.set_md.metadata['classes_order']       = self.dataset_md.metadata['classes_order']
                self.set_md.metadata['parental_name']       = self.dataset_md.metadata['name']
                self.set_md.metadata['serial_identifier']   = self._helper.getSerialNow()
                self.set_md.metadata['created_at']          = self._helper.getTimeNow()
                self.set_md.metadata['finished_at']         = ""
                self.set_md.metadata['train_images']        = {}
                self.set_md.metadata['validation_images']   = {}
                self.set_md.metadata['test_images']         = {}
                self.set_md.metadata['kootstrap_version']   = self._k.config['version']
                self.set_md.metadata['scissor']             = "yes"
                self.set_md.metadata['scissor_rate']        = float(self._k.scissor['target_rate'])
                self.set_md.metadata['scissor_min_with']    = int(self._k.scissor['target_min_width'])
                self.set_md.metadata['scissor_min_height']  = int(self._k.scissor['target_min_height'])
                self.set_md.metadata['slicer_type']         = 'total'
                self.set_md.metadata['train_proporcional_size']         = self._k.config['train_proportional_size']
                self.set_md.metadata['validation_proporcional_size']    = self._k.config['validation_proportional_size']
                self.set_md.metadata['test_proporcional_size']          = self._k.config['test_proportional_size']
                if self._k.config['file_order_randomly']:
                    self.set_md.metadata['file_order_randomly'] = 'yes'
                else:
                    self.set_md.metadata['file_order_randomly'] = 'no'
            else:
                self.set_md.metadata['train_images']        = {}
                self.set_md.metadata['validation_images']   = {}
                self.set_md.metadata['test_images']         = {}
            self.set_md.save()
            
            # train set
            path_folder_origin_classes = self.path_folder_origin+"train/"
            classes = [dI for dI in os.listdir(path_folder_origin_classes) if os.path.isdir(os.path.join(path_folder_origin_classes,dI))]
            print 'Class ',classes
            for class_name in classes:
                self.set_md.metadata['train_images'][class_name] = []
                self.set_md.save()
                
                files_to_transfer = glob.glob(path_folder_origin_classes+class_name+"/*.*")
                
                files_names = []
                #print "FILES to TRASNFER",files_to_transfer
                for file in files_to_transfer:
                    files_names.append(file.split("/")[-1:][0])
                    
                for file_name in files_names:
                    if os.path.isfile(os.path.join(path_folder_origin_classes+class_name+"/",file_name)) and file_name != ".DS_Store" and os.stat(path_folder_origin_classes+class_name+"/"+file_name ).st_size!=0:
                        self.set_md.metadata['train_images'][class_name].append(file_name)
                    else:
                        print "NOT FILE"
            self.set_md.save()
            
            # validation set
            path_folder_origin_classes = self.path_folder_origin+"validation/"
            classes = [dI for dI in os.listdir(path_folder_origin_classes) if os.path.isdir(os.path.join(path_folder_origin_classes,dI))]
            print 'Class ',classes
            for class_name in classes:
                self.set_md.metadata['validation_images'][class_name] = []
                self.set_md.save()
                
                files_to_transfer = glob.glob(path_folder_origin_classes+class_name+"/*.*")
                
                files_names = []
                #print "FILES to TRASNFER",files_to_transfer
                for file in files_to_transfer:
                    files_names.append(file.split("/")[-1:][0])
                    
                for file_name in files_names:
                    if os.path.isfile(os.path.join(path_folder_origin_classes+class_name+"/",file_name)) and file_name != ".DS_Store" and os.stat(path_folder_origin_classes+class_name+"/"+file_name ).st_size!=0:
                        self.set_md.metadata['validation_images'][class_name].append(file_name)
                    else:
                        print "NOT FILE"
            self.set_md.save()
            
            # validation set
            path_folder_origin_classes = self.path_folder_origin+"test/"
            classes = [dI for dI in os.listdir(path_folder_origin_classes) if os.path.isdir(os.path.join(path_folder_origin_classes,dI))]
            print 'Class ',classes
            for class_name in classes:
                self.set_md.metadata['test_images'][class_name] = []
                self.set_md.save()
                
                files_to_transfer = glob.glob(path_folder_origin_classes+class_name+"/*.*")
                
                files_names = []
                #print "FILES to TRASNFER",files_to_transfer
                for file in files_to_transfer:
                    files_names.append(file.split("/")[-1:][0])
                    
                for file_name in files_names:
                    if os.path.isfile(os.path.join(path_folder_origin_classes+class_name+"/",file_name)) and file_name != ".DS_Store" and os.stat(path_folder_origin_classes+class_name+"/"+file_name ).st_size!=0:
                        self.set_md.metadata['test_images'][class_name].append(file_name)
                    else:
                        print "NOT FILE"
            self.set_md.save()
            
        elif "weights" in sub_folders_origin:
            print "Model can't be recovery yet. Try a dataset or subset"
        else:
            print "We can't recovery from this directory. Try a dataset or subset"
            
            