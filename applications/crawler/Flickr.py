#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib,json,time,os,sys,glob

from wand.image import Image
from time import sleep
from threading import Thread

sys.path.append('../')

from system.Helper import Helper
from system.Logger import Logger
from system.Kootstrap import Kootstrap
class Flickr(Thread):
    
    _k                  = None
    
    _helper             = None
    _logger             = None
    _crawler_md         = None
    
    _path_dataset       = None
    _class_name         = None
    _year               = None
    _month              = None
    _day                = None
    
    _start_time         = None
    _end_time           = None
    _elapsed_time       = None
    
    _current_photo      = None
    _current_page       = None
    
    images_metadata     = None
    total_images        = None
    num_img_to_download = None
    
    url                 = None
    
    
    def __init__(self,crawler_md,class_name,tags,num_img_to_download,year,month,day,logger=None):
        Thread.__init__(self)
        
        self._helper        = Helper()
        self._k             = Kootstrap()
        
        if logger == None:
            self._logger    = Logger()
        else:
            self._logger    = logger
        
        self._crawler_md    = crawler_md
        
        self._class_name    = class_name
        self._tags          = tags
        self._year          = year
        self._month         = month
        self._day           = day
        
        self.num_img_to_download    = num_img_to_download
        self._path_dataset_class    = self._crawler_md.metadata['path_dataset']+"classes/"+self._class_name+"/"
        
        self.total_images   = 0
        self.total_pages    = 0
        self.total_imagens  = 0
        self.images_metadata= []
        self._current_photo = 0
        self._current_page  = 0
        self._session       = {}
        
        self._logger.info('Flickr: Date '+str(self._year)+'-'+str(self._month)+'-'+str(self._day))
        
    def run(self):
        
        # while the url is not empty:
        #   url = url configured to corrent page
        #   if data contains photos:
        #       if the page is the first:
        #           set the information about total images and pages
        #       for photo in photos:
        #           if photo not exist on mongod:
        #               get sizes_photo from photo
        #               get the best resolution form list
        #               set information on db
        #               --- download files
        #            else:
        #               set to image on the current session
        #       set the current page
        #       if current page is the last page:
        #           set url has empty
        #       else:
        #           set page has page plus one
        #   else:
        #       print the error data
        #       set url has empty
        
        self.url            = "initial"
        while self.url != None or self.num_img_to_download != 0 :
            print 'Data url',self.url,' self.num_img_to_download',self.num_img_to_download
            data = self.flickrGetPage(self._current_page)
            
            if 'photos' in data:
                #print 'Data'
                #print data
                self._logger.info('Flickr: '+str(len(data['photos']))+' images at '+str(self._current_page)+" page")
                self._current_page += 1
                if self._current_page == 1:
                    
                    self.total_imagens = int(data['photos']['total'])
                    self.total_pages = int(data['photos']['pages'])
                    self._logger.info("Flickr: The date "+str(self._year)+"-"+str(self._month)+"-"+str(self._day)+" has "+str(self.total_imagens)+" photos in "+str(self.total_pages)+" pages to download")
                    
                for photo in data['photos']['photo']:
                    
                    if self.num_img_to_download == 0:
                        self._logger.info("Flickr: Total of images has downloaded")
                        self.url = None
                        return
                        
                    self._current_photo     += 1
                    
                    image_on_dir = list(glob.glob(self._path_dataset_class+photo['id']+"*"))
                        
                    if len(image_on_dir) == 0:
                        
                        if photo['ispublic'] == 1:
                            visible = True
                        else:
                            visible = False

                        dataSizes = self.flickrGetPhotoSizes(photo['id'])
                        
                        max_width = 0
                        the_best_size = None
                        if 'sizes' in dataSizes:
                            #print 'creating images'
                            
                            for size in dataSizes['sizes']['size']:
                                if int(size['width']) > int(self._k.flickr['flickr_size_minimum_width']) and int(size['width'])< int(self._k.flickr['flickr_size_maximum_width']) and int(size['height']) > int(self._k.flickr['flickr_size_minimum_height']) and int(size['height'])< int(self._k.flickr['flickr_size_maximum_height']):
                                    the_best_size = size
                                    
                            if the_best_size == None:
                                max_width = 0
                                for size in dataSizes['sizes']['size']:
                                    if max_width <= int(size['width']) and int(size['width']) <= self._k.flickr['flickr_size_maximum_width']:
                                        max_width = int(size['width'])
                                        the_best_size = size
                            
                            if int(the_best_size['width']) >= int(self._k.flickr['flickr_size_minimum_width']) and int(the_best_size['height']) >= int(self._k.flickr['flickr_size_minimum_height']):
                                
                                #print the_best_size['width'], the_best_size['height'],int(self._k.flickr['flickr_size_minimum'])
                                
                                name = the_best_size['source'].split('/')
                                name = name[len(name)-1]
                                name = name.replace("?zz=1","")

                                self.createFileOnRepository( self._path_dataset_class, name, the_best_size['source'])

                                self.images_metadata.append({'flickr_id':photo['id'], 'width':the_best_size['width'],'height':the_best_size['height'],'visible':visible,'name':name})

                                self.num_img_to_download-=1
                                self.total_images       +=1

                                self._logger.info('Flickr: Creating the image '+photo['id']+' with '+str(the_best_size['width'])+'x'+str(the_best_size['height'])+'. Still missing '+str(self.num_img_to_download)+" images")
                            else:
                                self._logger.info('Flickr: Can\'t create the image '+photo['id']+' '+str(the_best_size['width'])+'x'+str(the_best_size['height'])+". Because is too short")
                        else:
                            self._logger.error('Flickr: Oh no! erro at download sizes of images =O')
                        
                    else:
                        if self._k.config['file_exist_count_has_download']:
                            self.num_img_to_download-=1
                            self.total_images       +=1
                        self._logger.info('Flickr: The image id '+photo['id']+' has crawled after')
                        
                self._current_page = int(data['photos']['page'])
                if self._current_page >= self.total_pages:
                    print '!!!-->',self._current_page,"-",self.total_pages
                    self.url = None
                    self.num_img_to_download = 0
                else:
                    self._logger.info("Flickr: "+str(self._current_page)+' from '+str(self.total_pages)+' pages')
                print '-->',self._current_page,"-",self.total_pages
                self._logger.info("Flickr: "+str(self._current_photo)+' from '+str(self.total_imagens)+' images')
                
            else:
                self._current_page +=1
                self._logger.critical('Flickr: Dammit! The information block not return what we want :S')
                print 'Error on data'
                print data
                self.url = None
            
            
    def flickrGetPage(self,page):
        self.url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&tags="+self._tags+"&api_key="+self._k.flickr['flickr_public_key']+"&format=json&nojsoncallback=?&page="+str(page)+"&per_page="+str(self._k.flickr['flickr_per_page'])+"&min_upload_date="+str(self._year)+"-"+str(self._month)+"-"+str(self._day)+"%2000:00:00&max_upload_date="+str(self._year)+"-"+str(self._month)+"-"+str(self._day)+"%2023:59:59"
        self._logger.info('Flickr: flickrGetPage page '+str(page)+' :D')
        self._start_time = time.time()
        print 'Page url'
        print self.url 
        response = urllib.urlopen(self.url)
        data = json.loads(response.read())
        self._end_time = time.time()


        # check if elapsed time between start and end the executation
        #   ocourred in 1 second. Less that 1 second the thread slepp
        #   the rest
        self._elapsed_time = self._end_time - self._start_time
        if self._elapsed_time < 1.0 and self._k.flickr['safe_mode']:
            sleep_for = 1.0 - self._elapsed_time
            self._logger.info('Flickr: flickrGetPage need Zzz for '+str(sleep_for))
            sleep(sleep_for)
            
        return data
    
    def flickrGetPhotoInfo(self,photo_id):  
        self.url = "https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&photo_id="+photo_id+"&api_key="+self._k.flickr['flickr_public_key']+"&format=json&nojsoncallback=?"
        #self._logger.info('Flickr: flickrGetPhotoInfo to '+photo_id+' :D')
        self._start_time = time.time()
        response = urllib.urlopen(self.url)
        data = json.loads(response.read())
        self._end_time = time.time()


        # check if elapsed time between start and end the executation
        #   ocourred in 1 second. Less that 1 second the thread slepp
        #   the rest
        self._elapsed_time = self._end_time - self._start_time
        if self._elapsed_time < 1.0 and self._k.flickr['safe_mode']:
            sleep_for = 1.0 - self._elapsed_time
            #self._logger.info('Flickr: flickrGetPhotoInfo need Zzz for '+str(sleep_for))
            sleep(sleep_for)
        return data
    
    def flickrGetPhotoSizes(self,photo_id): 
        self.url = "https://api.flickr.com/services/rest/?method=flickr.photos.getSizes&photo_id="+photo_id+"&api_key="+self._k.flickr['flickr_public_key']+"&format=json&nojsoncallback=?"
        #self._logger.info('Flickr: flickrGetPhotoSizes to '+photo_id+' :D')
        self._start_time = time.time()
        response = urllib.urlopen(self.url)
        data = json.loads(response.read())
        self._end_time = time.time()


        # check if elapsed time between start and end the executation
        #   ocourred in 1 second. Less that 1 second the thread slepp
        #   the rest
        self._elapsed_time = self._end_time - self._start_time
        if self._elapsed_time < 1.0 and self._k.flickr['safe_mode']:
            sleep_for = 1.0 - self._elapsed_time
            #self._logger.info('Flickr: flickrGetPhotoSizes need Zzz for '+str(sleep_for))
            sleep(sleep_for)
        return data
    
    def createFileOnRepository(self,directory,file_name,url):
        #self._logger.info('Flickr: createFileOnRepository file '+file_name+' :)')
        file_photo = urllib.urlopen(url)
        with open(directory+file_name,'wb') as output:
            output.write(file_photo.read())