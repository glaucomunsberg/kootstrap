#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse,sys, traceback

sys.path.append('../')

from system.Koopstrap import Koopstrap
from system.Metadata import Metadata
from system.Logger import Logger
from system.Helper import Helper
from Dataset import Dataset
from Flickr import Flickr

class Crawler:
    
    _k      = None # koopstrap
    _logger = None
    _helper = None
    _args   = None
    
    dataset         = None
    tags_by_class   = None
    num_images      = None
    crawler_md      = None
    
    def __init__(self,args):
        
        self._k         = Koopstrap()
        self._logger    = Logger(app_name='Crawler')
        self._helper    = Helper()
        self._args      = args
        self.dataset    = Dataset(args, self._logger)
        self.num_images = args.num_images
    
        self.tags_by_class  = []
        
        if args.flickr_tags_load_file != None:
            file = open(args.flickr_tags_load_file,'r')
            for line in file:
                line = line.replace('\n', '').replace('\r', '')
                self.tags_by_class.append(line)
        else:
            for line in args.flickr_tags.split(","):
                line = line.replace('\n', '').replace('\r', '')
                self.tags_by_class.append(line)
                
        serial = self._helper.getSerialNow()
        self.crawler_md = Metadata(self.dataset.dataset_path+"metadata_crawler_"+serial+".json", create_file=True)
        
    def start(self):
        
        self.dataset.start()
        
        self._logger.info("Crawler: Flickr tags: {0}".format(self.tags_by_class))
        self._logger.info("Crawler: Flickr year min '{0}' and max {1}".format(self._k.flickr['flickr_year_min'],self._k.flickr['flickr_year_max']))
        self._logger.info("Crawler: Flickr size '{0}'. The min size is {1} and max size is {2}".format(self._k.flickr["flickr_size"],self._k.flickr["flickr_size_minimum_width"],self._k.flickr["flickr_size_maximum_width"]))
        self._logger.info("Crawler: Flickr max of images by class '{0}'".format(self.num_images))
        
        self.crawler_md.metadata['flickr_year_min'] = self._k.flickr['flickr_year_min']
        self.crawler_md.metadata['flickr_year_max'] = self._k.flickr['flickr_year_max']
        self.crawler_md.metadata['flickr_size_minimum'] = self._k.flickr['flickr_size_minimum_width']
        self.crawler_md.metadata['flickr_size_maximum'] = self._k.flickr['flickr_size_maximum_width']
        self.crawler_md.metadata['path_dataset'] = self.dataset.dataset_path
        self.crawler_md.metadata['total_images_by_class'] = self.num_images
        self.crawler_md.metadata['created_at'] = self._helper.getTimeNow()
        self.crawler_md.metadata['classes_images'] = {}
        self.crawler_md.save()
        
        position = 0
        for class_name in self.dataset.classes:
            
            self.crawler_md.metadata['classes_images'][class_name] = []
            self.crawler_md.save()
            
            tags = self.tags_by_class[position]
            self._logger.info("Crawler: Start classe '{0}' whit tags '{1}' ".format( class_name, tags ))
            
            num_img_to_download = self._args.num_images
            
            for year in range(self._k.flickr['flickr_year_min'],self._k.flickr['flickr_year_max']+1):
                for month in range(1,13):
                    for day in range(1,32):
                        executation_not_done = True
                        while executation_not_done and num_img_to_download != 0:
                            try:
                                flickr = Flickr(self.crawler_md,class_name,tags,num_img_to_download,year,month,day,self._logger)
                                flickr.run()
                                executation_not_done = False
                                num_img_to_download -= flickr.total_images
                                self.crawler_md.metadata['classes_images'][class_name] += flickr.images_metadata
                                self.crawler_md.save()
                                
                                self.dataset.dataset_md.metadata['classes'][class_name]['num_images'] += len(flickr.images_metadata)
                                self.dataset.dataset_md.metadata['classes'][class_name]['images'] += [x['name'] for x in flickr.images_metadata]
                
                                self.dataset.dataset_md.save()
                            except Exception as error:
                                executation_not_done = True
                                self._logger.error('Crawler: something was wrong at data '+str(year)+'/'+str(month)+' :/ I need stop the job!')
                                print traceback.format_exc()
                                self._logger.error('Flicker:'+str(traceback.format_exc()))
            position+=1
                            
        self._logger.info("Crawler: end correctly")