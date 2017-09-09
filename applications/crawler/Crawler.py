#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse,sys, traceback

sys.path.append('../')

from system.Kootstrap import Kootstrap
from system.Metadata import Metadata
from system.Logger import Logger
from system.Helper import Helper
from maker.Dataset import Dataset
from maker.Compiler import Seeder
from Flickr import Flickr

class Crawler:
    
    _k      = None # kootstrap
    _logger = None
    _helper = None
    _args   = None
    
    dataset         = None
    tags_by_class   = None
    classes         = None
    num_images      = None
    crawler_md      = None
    dataset_md      = None
    
    def __init__(self,args):
        
        self._k         = Kootstrap()
        self._logger    = Logger(app_name='Crawler')
        self._helper    = Helper()
        self._args      = args
        self.num_images = args.num_images
    
        self.tags_by_class  = []
        self.classes        = []
        
        self.dataset_md = Metadata(self._k.path_dataset()+args.dataset_name+"/metadata.json")
        
        if args.flickr_tags_load_file != None:
            self.tags_by_class = self._helper.filePathToList(args.flickr_tags_load_file)
        else:
            for line in args.flickr_tags.split(","):
                line = line.replace('\n', '').replace('\r', '')
                self.tags_by_class.append(line)
            
        if args.classes_load_file != None:
            self.classes = self._helper.filePathToList(args.classes_load_file)
        else:
            if args.classes != None:
                for line in args.classes.split(","):
                    line = line.replace('\n', '').replace('\r', '')
                    self.classes.append(line)
            else:
                self.classes = self.dataset_md.metadata['classes_order']
                
        if len(self.tags_by_class) != len(self.classes) :
            raise ValueError('Number of classes {0} and number of tags by class {1} is not the same'.format(len(self.tags_by_class),len(self.classes)))
            
        serial = self._helper.getSerialNow()
        self.crawler_md = Metadata(self._k.path_dataset()+args.dataset_name+"/metadata_crawler_"+serial+".json", create_file=True)
        
    def start(self):
        
        self._logger.info("Crawler: Flickr tags: {0}".format(self.tags_by_class))
        self._logger.info("Crawler: Flickr year min '{0}' and max {1}".format(self._k.flickr['flickr_year_min'],self._k.flickr['flickr_year_max']))
        self._logger.info("Crawler: The min size is {0} and max size is {1}".format(self._k.flickr["flickr_size_minimum_width"],self._k.flickr["flickr_size_maximum_width"]))
        self._logger.info("Crawler: Flickr max of images by class '{0}'".format(self.num_images))
        
        self.crawler_md.metadata['flickr_year_min'] = self._k.flickr['flickr_year_min']
        self.crawler_md.metadata['flickr_year_max'] = self._k.flickr['flickr_year_max']
        self.crawler_md.metadata['flickr_size_minimum'] = self._k.flickr['flickr_size_minimum_width']
        self.crawler_md.metadata['flickr_size_maximum'] = self._k.flickr['flickr_size_maximum_width']
        self.crawler_md.metadata['path_dataset'] = self._k.path_dataset()+self._args.dataset_name+"/"
        self.crawler_md.metadata['total_images_by_class'] = self.num_images
        self.crawler_md.metadata['created_at'] = self._helper.getTimeNow()
        self.crawler_md.metadata['finished_at'] = ""
        self.crawler_md.metadata['kootstrap_version'] = self._k.config['version']
        self.crawler_md.metadata['classes_images'] = {}
        self.crawler_md.save()
        
        position = 0
        for class_name in self.classes:
            
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
                                
                                self.dataset_md.metadata['classes'][class_name]['num_images'] += len(flickr.images_metadata)
                                self.dataset_md.metadata['classes'][class_name]['images'] += [x['name'] for x in flickr.images_metadata]
                                
                                self.dataset_md.save()
                            except Exception as error:
                                executation_not_done = True
                                self._logger.error('Crawler: something was wrong at data '+str(year)+'/'+str(month)+' :/ I need stop the job!')
                                print traceback.format_exc()
                                self._logger.error('Flicker:'+str(traceback.format_exc()))
            position+=1
            
        
        if self._args.feed_subsets == "yes":
            seeder = Seeder(self._k.path_dataset()+self._args.dataset_name+"/", self.crawler_md.metadata['classes_images'], self._logger)
            seeder.seed()
            
        self.crawler_md.metadata['finished_at'] = self._helper.getTimeNow()
        self.crawler_md.save()
        self._logger.info("Crawler: end correctly")