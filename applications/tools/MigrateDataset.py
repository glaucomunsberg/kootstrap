import os, argparse, sys, glob, shutil, random
sys.path.append('../')

from system.Kootstrap import Kootstrap
from system.Metadata import Metadata
from system.Logger import Logger
from system.Helper import Helper
from maker.Dataset import Dataset

class MigrateDataset:
    
    _k      = None
    _args   = None
    _helper = None
    _logger = None
    
    set_md          = None
    is_a_set_type   = None
    
    original_path_destiny   = None
    computed_path_destiny   = None
    original_path_origin    = None
    metadata_path           = None
    
    number_of_images_by_class   = None
    copy_way                    = None
    def __init__(self,args):
        
        self._k         = Kootstrap()
        self._helper    = Helper()
        self._logger    = Logger('Tools')
        
        self.original_path_destiny = os.path.abspath(args.path_destiny)
        self.original_path_origin   = os.path.abspath(args.path_origin)
        
        self._logger.info("Transfer: path origin '{0}'".format(self.original_path_origin))
        self._logger.info("Transfer: path destiny '{0}'".format(self.original_path_destiny))
        
        
        if args.max_files_by_class < 0:
            self.number_of_images_by_class = float('inf')
        else:
            self.number_of_images_by_class = args.max_files_by_class
        
        if self.original_path_origin[-1:] != "/":
            self.original_path_origin+="/"
            
        if self.original_path_destiny[-1:] != "/":
            self.original_path_destiny+="/"
            
        if not os.path.exists(self.original_path_origin):
            self._logger.info("arg --path_origin is not a valid path")
            raise ValueError('arg --path_origin is not a valid path')
            
        if not os.path.exists(self.original_path_destiny):
            self._logger.info("arg --path_destiny is not a valid path")
            raise ValueError('arg --path_destiny is not a valid path')
        
        if os.path.isfile(self.original_path_destiny+"metadata.json"):
            self.metadata_path  = self.original_path_destiny+"metadata.json"
            self.set_md = Metadata(self.metadata_path)
        elif os.path.isfile(self.original_path_destiny+"../metadata.json"):
            self.metadata_path  = os.path.abspath(self.original_path_destiny+"../metadata.json")
            self.set_md = Metadata(self.metadata_path)
            
        elif os.path.isfile(self.original_path_destiny+"../../metadata.json"):
            self.metadata_path  = os.path.abspath(self.original_path_destiny+"../../metadata.json")
            self.set_md = Metadata(self.metadata_path)
        else:
            bits_path = self.original_path_destiny.split("/")
            if bits_path[-1:][0] == "":
                del bits_path[len(bits_path)-1]
                
            if bits_path[-1:][0] in ["datasets","data","kootstrap"]:
                self.is_a_set_type  = "datasets"
            else:
                raise ValueError("arg --path_destiny is not inside a class from dataset or subset much less in a metadata.json folder: "+self.original_path_destiny+" a sub: "+self.original_path_destiny.split("/")[-1:][0])
        
        if self.is_a_set_type == None:
            if "parental_name" in self.set_md.metadata.keys():
                self.is_a_set_type  = "subset"
            else:
                self.is_a_set_type  = "dataset"
                
        if args.copy_way in ["copy","move"]:
            self.copy_way = args.copy_way
        elif args.copy_way == None:
            self.copy_way = self._k.config['transfer_file_type'] 
        else:
            self._logger.info("Transfer: --copy_way needed")
            raise ValueError('arg --copy_way need be ignored or a string with copy or move.')
        
        self._logger.info("Transfer: Type '{0}'".format(self.is_a_set_type))
        
    def start(self):
        
        sub_folders_destiny = [dI for dI in os.listdir(self.original_path_destiny) if os.path.isdir(os.path.join(self.original_path_destiny,dI))]
        sub_folders_origin = [dI for dI in os.listdir(self.original_path_origin) if os.path.isdir(os.path.join(self.original_path_origin,dI))]
        
        if self.is_a_set_type == "datasets":
            self.createANewDataset()
        elif self.is_a_set_type == "dataset" or self.is_a_set_type == "subset":
            print "You can't migrate to subset or into a dataset"
            
    def createANewDataset(self):
        
        sub_folders_origin = [dI for dI in os.listdir(self.original_path_origin) if os.path.isdir(os.path.join(self.original_path_origin,dI))]
        
        dataset_name    = ""
        class_name      = ""
        annotation      = ""
        
        if len(sub_folders_origin) == 0:
            
            files_in_directory = glob.glob(self.original_path_origin+"*.*")
        
            value = raw_input("Do you wanna create a dataset with ONE class with {0} images from '{1}' folder? y/n".format(len(files_in_directory),self.original_path_origin.split("/")[-1:][0])) 
            
            if value.upper() == "Y":
                dataset_name    = raw_input("Dataset name (not empty):")
                class_name      = raw_input("Class name (not empty):")
                annotation      = raw_input("Dataset annotation:")
                if dataset_name == "" or dataset_name == None or class_name == "" or class_name == None:
                    print "Dataset or Class name can't be empty"
                    return ""
                if class_name != Dataset.normalizeDatasetName(class_name):
                    class_name = Dataset.normalizeDatasetName(class_name)
                    print "Attencion: The name of class was normalize to '{0}'.".format(class_name)
            else:
                print "OK bye"
                return ""
        else:
            value = raw_input("Do you wanna create a dataset with {0} classes ? y/n ".format( len( sub_folders_origin ) ) ) 
            if value.upper() == "Y":
                dataset_name    = raw_input("Dataset name (not empty):")
                annotation      = raw_input("Dataset annotation:")
                if dataset_name == "" or dataset_name == None:
                    print "Dataset name can't be empty"
                    return ""
            else:
                print "OK bye"
                return ""
        
        # check the name
        if dataset_name != Dataset.normalizeDatasetName(dataset_name):
            dataset_name = Dataset.normalizeDatasetName(dataset_name)
            print "Attencion: The name of dataset was normalize to '{0}'.".format(dataset_name)
            
        # create the folder 
        path_new_dataset            = self._k.path_dataset()+dataset_name+"/"
        path_classes_new_dataset    = path_new_dataset+"classes/"
        
        if not os.path.exists(path_new_dataset):
            os.makedirs(path_new_dataset)
            os.makedirs(path_classes_new_dataset)
        else:
            print "you can't create two dataset with same name"
            return ""
        self._logger.info("Transfer: New Dataset name       '{0}'".format(dataset_name))
        self._logger.info("Transfer: New Dataset classes    '{0}'".format(sub_folders_origin))
        self._logger.info("Transfer: New Dataset annotation '{0}'".format(annotation))
        
        new_dataset_md = Metadata(path_new_dataset+"metadata.json",True)
        new_dataset_md.metadata['name'] = dataset_name
        new_dataset_md.metadata['serial_identifier'] = self._helper.getSerialNow()
        new_dataset_md.metadata['created_at'] = self._helper.getTimeNow()
        new_dataset_md.metadata['classes'] = {}
        new_dataset_md.metadata['classes_order'] = sub_folders_origin
        new_dataset_md.metadata['annotation'] = annotation
        new_dataset_md.save()
        
        if len(sub_folders_origin) == 0:
            
            moved = 0
            class_destiny_path = path_classes_new_dataset+class_name+"/"
            os.makedirs(class_destiny_path)
            
            files_to_transfer = glob.glob(self.original_path_origin+"*.*")
            
            if self._k.config['file_order_randomly'] == True:
                random.shuffle(files_to_transfer)
            files_names = []
            for file in files_to_transfer:
                files_names.append(file.split("/")[-1:][0])
            
            new_dataset_md.metadata['classes'][class_name] = {}
            new_dataset_md.metadata['classes'][class_name]['num_images'] = 0
            new_dataset_md.metadata['classes'][class_name]['images'] = []
            new_dataset_md.save()
            
            for file_name in files_names:
                if os.path.isfile(os.path.join(self.original_path_origin,file_name)) and file_name != ".DS_Store" and os.stat(self.original_path_origin+file_name).st_size!=0:
                    if moved < self.number_of_images_by_class:
                        if self.copy_way:
                            self._logger.info("Transfer: Copy {0} file '{2}' to class '{1}'".format(moved, class_name, file_name))
                            shutil.copyfile(self.original_path_origin+file_name, class_destiny_path+file_name)
                        else:
                            self._logger.info("Transfer: Moving {0} file '{2}' to class '{1}'".format(moved, class_name, file_name))
                            shutil.move(self.original_path_origin+file_name, class_destiny_path+file_name)
                        moved+=1
                        new_dataset_md.metadata['classes'][class_name]['num_images'] += 1
                        new_dataset_md.metadata['classes'][class_name]['images'].append(file_name)
            new_dataset_md.save()
        else:
            for class_name in sub_folders_origin:
                moved = 0
                class_destiny_path = path_classes_new_dataset+class_name+"/"
                os.makedirs(class_destiny_path)

                files_to_transfer = glob.glob(self.original_path_origin+class_name+"/*.*")
                print 'path:             ',self.original_path_origin+class_name+"/*.*"
                print 'files_to_trasnfer:',files_to_transfer
                
                if self._k.config['file_order_randomly'] == True:
                    random.shuffle(files_to_transfer)
                files_names = []
                for file in files_to_transfer:
                    files_names.append(file.split("/")[-1:][0])

                new_dataset_md.metadata['classes'][class_name] = {}
                new_dataset_md.metadata['classes'][class_name]['num_images'] = 0
                new_dataset_md.metadata['classes'][class_name]['images'] = []
                new_dataset_md.save()

                for file_name in files_names:
                    if os.path.isfile(os.path.join(self.original_path_origin+class_name+"/",file_name)) and file_name != ".DS_Store" and os.stat( self.original_path_origin+class_name+"/"+file_name ).st_size!=0:
                        if moved < self.number_of_images_by_class:
                            if self.copy_way:
                                self._logger.info("Transfer: Copy {0} file '{2}' to class '{1}'".format(moved, class_name, file_name))
                                shutil.copyfile(self.original_path_origin+class_name+"/"+file_name, class_destiny_path+file_name)
                            else:
                                self._logger.info("Transfer: Moving {0} file '{2}' to class '{1}'".format(moved, class_name, file_name))
                                shutil.move(self.original_path_origin+class_name+"/"+file_name, class_destiny_path+file_name)
                            moved+=1
                            new_dataset_md.metadata['classes'][class_name]['num_images'] += 1
                            new_dataset_md.metadata['classes'][class_name]['images'].append(file_name)
                new_dataset_md.save()
                
        print 'Finish! You have a dataset migrated!'