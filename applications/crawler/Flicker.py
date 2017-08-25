#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib,json,time,os

from wand.image import Image
from time import sleep
from threading import Thread

from system.Helper import Helper
from system.Logger import Logger

class Flickr(Thread):
    
    _identifier         = None
    
    _mongo              = None
    _config             = None
    _helper             = None
    _logger             = None
    
    _session_at_mongo   = None
    _start_time         = None
    _end_time           = None
    _elapsed_time       = None
    _current_photo      = None
    _current_page       = None
    
    _prompt             = None
    
    url                 = None
    
    def __init__(self,session_identifier,prompt,year,month,day):
        Thread.__init__(self)
        
        self._identifier    = session_identifier
        
        self._mongo         = Mongo()
        self._config        = Configuration()
        self._helper        = Helper()
        self._logger        = Logger()
        
        self._year          = year
        self._month         = month
        self._day           = day
        
        self._current_photo = 0
        self._current_page  = 0
        self._session_at_mongo   = self._mongo.getCrawlerById(self._identifier)
        
        self._prompt        = prompt
        
        filename = self._config.flickr_folder+'README.md'
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        self._logger.info('Flicker: Start in date '+str(self._year)+'-'+str(self._month)+'-'+str(self._day))
        
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
        while self.url != None :
                
            data = self.flickrGetPage(self._session_at_mongo['current_page'])
            
            if 'photos' in data:
                self._current_page += 1
                if self._session_at_mongo['current_page'] == 1:
                    #print 'total'
                    #print data['photos']['total']
                    #print 'Pages'
                    #print data['photos']['pages']
                    #print 'Page'
                    #print data['photos']['page']
                    #print 'Photos'
                    #print data['photos']['photo']
                    self._session_at_mongo['total_imagens'] = int(data['photos']['total'])
                    self._session_at_mongo['total_pages'] = int(data['photos']['pages'])
                    self._logger.info("Flicker: The date "+str(self._year)+"-"+str(self._month)+"-"+str(self._day)+" has "+str(self._session_at_mongo['total_imagens'])+" photos in "+str(self._session_at_mongo['total_pages'])+" pages to download")
                for photo in data['photos']['photo']:
                    
                    self._current_photo += 1
                    
                    #self._logger.info(str(self._current_photo)+' from '+str(self._session_at_mongo['total_imagens'])+' photos')
                    
                    image_on_mongo = self._mongo.getFlickrImageById(photo['id'])
                    if image_on_mongo == None:
                        
                        if self._prompt:
                            print str(self._current_photo)+' from '+ str(self._session_at_mongo['total_imagens'])+ ' photos'
                        
                        if photo['ispublic'] == 1:
                            visible = True
                        else:
                            visible = False

                        image_on_mongo_id = self._mongo.insertFlickrImage(self._helper.getSerialNow(), photo['id'],[self._identifier], self._helper.getTimeNow(), 0, 0, "", "", visible)
                        
                        self._logger.info('Flicker: The image id '+photo['id']+' is new on repository! ;)')
                        
                        #dataPhoto = self.flickrGetPhotoInfo(photo['id'])
                        dataSizes = self.flickrGetPhotoSizes(photo['id'])
                        
                        max_width = 0
                        the_best_size = None
                        if 'sizes' in dataSizes:
                            #print 'creating images'
                            
                            if self._config.flickr_size == "small":
                                for size in dataSizes['sizes']['size']:
                                    if size['label'] == "Small":
                                        the_best_size = size
                                if the_best_size == None:
                                    max_width = 99999
                                    for size in dataSizes['sizes']['size']:
                                        if max_width >= int(size['width']) and int(size['width']) >= self._config.flickr_size_minimum:
                                            max_width = int(size['width'])
                                            the_best_size = size
                                        
                            elif self._config.flickr_size == "medium":
                                list_of_sizes = []
                                for size in dataSizes['sizes']['size']:
                                    list_of_sizes.append(int(size['width']))
                                    list_of_values = sorted(list_of_values, key=int)
                                    the_best_with = len(list_of_values)/2
                                for size in dataSize['sizes']['size']:
                                    if the_best_with == size['width']:
                                        the_best_size = size
                            else:
                                max_width = 0
                                for size in dataSizes['sizes']['size']:
                                    if max_width <= int(size['width']) and int(size['width']) <= self._config.flickr_size_maximum:
                                        max_width = int(size['width'])
                                        the_best_size = size
                            
                            name = the_best_size['source'].split('/')
                            name = name[len(name)-1]

                            self.createFileOnRepository(self._config.flickr_folder,name,the_best_size['source'])
                            
                            self._mongo.setUpdateFlickrImage(photo['id'], the_best_size['width'],the_best_size['height'], the_best_size['source'], self._config.flickr_folder+name)
                            self._logger.info('Flicker: Creating the image '+photo['id']+' with '+str(the_best_size['width'])+'x'+str(the_best_size['height']))
                                        
                        else:
                            self._logger.error('Flicker: Oh no! erro at download sizes of images =O')
                        
                    else:
                        if self._prompt:
                            print str(self._current_photo)+' (skipped) from '+ str(self._session_at_mongo['total_imagens'])+ ' photos'
                        self._logger.info('Flicker: The image id '+photo['id']+' has crawled after :)')
                        image_on_mongo['sessions'].append(self._identifier)
                        self._mongo.updateImageByIdentifier(image_on_mongo['image_flicker_id'],image_on_mongo)
                        
                self._session_at_mongo['current_page'] = int(data['photos']['page'])
                if self._session_at_mongo['current_page'] > self._session_at_mongo['total_pages']:
                    self.url = None
                else:
                    self._session_at_mongo['current_page'] += 1
                self._mongo.updateCrawlerByIdentifier(self._identifier,self._session_at_mongo)
                
                print str(self._current_photo)+' from '+str(self._session_at_mongo['total_imagens'])+' pages'
                self._logger.info(str(self._current_photo)+' from '+str(self._session_at_mongo['total_imagens'])+' pages')
                
            else:
                self._logger.critical('Flicker: Dammit! The information block not return what we want :S')
                print 'Error on data'
                print data
                self.url = None
            
            
    def flickrGetPage(self,page):
        self.url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&tags="+self._config.flickr_tags+"&api_key="+self._config.flickr_public_key+"&format=json&nojsoncallback=?&page="+str(page)+"&per_page="+str(self._config.flickr_per_page)+"&min_upload_date="+str(self._year)+"-"+str(self._month)+"-"+str(self._day)+"%2000:00:00&per_page=500&max_upload_date="+str(self._year)+"-"+str(self._month)+"-"+str(self._day)+"%2023:59:59"
        self._logger.info('Flicker: flickrGetPage page '+str(page)+' :D')
        self._start_time = time.time()
        response = urllib.urlopen(self.url)
        data = json.loads(response.read())
        self._end_time = time.time()


        # check if elapsed time between start and end the executation
        #   ocourred in 1 second. Less that 1 second the thread slepp
        #   the rest
        self._elapsed_time = self._end_time - self._start_time
        if self._elapsed_time < 1.0 and self._config.safe_mode:
            sleep_for = 1.0 - self._elapsed_time
            self._logger.info('Flicker: flickrGetPage need Zzz for '+str(sleep_for))
            sleep(sleep_for)
            
        return data
    
    def flickrGetPhotoInfo(self,photo_id):  
        self.url = "https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&photo_id="+photo_id+"&api_key="+self._config.flickr_public_key+"&format=json&nojsoncallback=?"
        #self._logger.info('Flicker: flickrGetPhotoInfo to '+photo_id+' :D')
        self._start_time = time.time()
        response = urllib.urlopen(self.url)
        data = json.loads(response.read())
        self._end_time = time.time()


        # check if elapsed time between start and end the executation
        #   ocourred in 1 second. Less that 1 second the thread slepp
        #   the rest
        self._elapsed_time = self._end_time - self._start_time
        #print 'Executation at'
        #print self._elapsed_time
        if self._elapsed_time < 1.0 and self._config.safe_mode:
            sleep_for = 1.0 - self._elapsed_time
            #self._logger.info('Flicker: flickrGetPhotoInfo need Zzz for '+str(sleep_for))
            sleep(sleep_for)
        return data
    
    def flickrGetPhotoSizes(self,photo_id): 
        self.url = "https://api.flickr.com/services/rest/?method=flickr.photos.getSizes&photo_id="+photo_id+"&api_key="+self._config.flickr_public_key+"&format=json&nojsoncallback=?"
        #self._logger.info('Flicker: flickrGetPhotoSizes to '+photo_id+' :D')
        self._start_time = time.time()
        response = urllib.urlopen(self.url)
        data = json.loads(response.read())
        self._end_time = time.time()


        # check if elapsed time between start and end the executation
        #   ocourred in 1 second. Less that 1 second the thread slepp
        #   the rest
        self._elapsed_time = self._end_time - self._start_time
        if self._elapsed_time < 1.0 and self._config.safe_mode:
            sleep_for = 1.0 - self._elapsed_time
            #self._logger.info('Flicker: flickrGetPhotoSizes need Zzz for '+str(sleep_for))
            sleep(sleep_for)
        return data
    
    def createFileOnRepository(self,directory,file_name,url):
        self._logger.info('Flicker: createFileOnRepository file '+file_name+' :)')
        file_photo = urllib.urlopen(url)
        with open(directory+file_name,'wb') as output:
            output.write(file_photo.read())