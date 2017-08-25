#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, json,platform
from Helper import Helper

class Logger:
        
    _instance   = None
    _helper     = None
    _metadata   = None
    _app_name   = None
    logging     = None
    
    def __init__(self,app_name='Koostrap',level='INFO'):
        
        self._helper = Helper()
        
        try:
            with open('../../data/configs/koopstrap.json','r') as f:
                self._metadata = json.load(f)
        except:
            None
            
        self.logging = logging
        
        self.logging.basicConfig( filename=self._metadata['path_root']+self._metadata['path_log']+self._helper.getSerialNow()+"_"+app_name+".log", level=logging.DEBUG )
        self.logging.Formatter(fmt='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        self.level              = level
        
        self.logging.info(self._helper.getTimeNow()+" Start at "+platform.platform()+" with "+platform.processor())
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
        return cls._instance
        
    def error(self,message):
        self.logging.error(self._helper.getTimeNow()+" "+message)
        
    def critical(self,message):
        self.logging.critical(self._helper.getTimeNow()+" "+message)
        
    def warning(self,message):
        self.logging.warning(self._helper.getTimeNow()+" "+message)
        
    def info(self,message):
        self.logging.info(self._helper.getTimeNow()+" "+message)

    def debug(self,message):
        self.logging.debug(self._helper.getTimeNow()+" "+message)