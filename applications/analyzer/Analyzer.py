import os, argparse, sys
sys.path.append('../')

from system.Metadata import Metadata
from system.Logger import Logger
from system.Helper import Helper
from tester.Tester import Tester
from Top import TopClass,TopHistogram
from Visualization import Visualization

class Analyzer:
    
    _args               = None
    _k                  = None
    
    path_test_folder            = None
    path_test_predictions_csv   = None
    
    predictions_csv     = None
    test_md             = None
    number_of_classes   = None
    
    def __init__(self,args):
        
        self.path_test_folder           = Tester.pathFromTestName(args.test_name)
        
        if args.mode == "top":
            if self.path_test_folder == None:
                raise ValueError('the --test_name is not valid test')
            if args.number_of_tops < 1:
                raise ValueError('the --number_of_tops need by great that 0')
        
            self.path_test_predictions_csv  = self.path_test_folder+"predictions.csv"
            self.test_md                    = Metadata(self.path_test_folder+"metadata.json")
        
            self.number_of_classes  = self.test_md.metadata['num_classes']
        self._args              = args
        
        self._logger            = Logger('Analyzer')
        
    def start(self):
        if self._args.mode == "top":
            topClass = TopClass(self.path_test_predictions_csv, self.path_test_folder, self._args.number_of_tops, self.number_of_classes, self._logger)
            topClass.start()
            topHistogram = TopHistogram(self._args,topClass.file_name_top_classes,self.path_test_folder,self.number_of_classes,self._logger)
            topHistogram.start()
        else:
            visualization = Visualization(self._args,self._logger)
            visualization.start()