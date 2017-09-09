#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, json,platform, os
from Helper import Helper
from Kootstrap import Kootstrap

class Logger:
        
    _instance   = None
    _helper     = None
    _k          = None
    
    _app_name   = None
    _path_logger= None
    logging     = None
    
    def __init__(self,app_name='Koostrap',level=None):
        
        self._helper        = Helper()
        self._k             = Kootstrap()
        self._app_name      = app_name
            
        self.logging        = logging
        self._path_logger   = self._k.path_log()+app_name.lower()+"/"
        
        if not os.path.exists(self._path_logger):
            os.makedirs(self._path_logger)
            
        if level == None:
            level = self._k.config['log_level']
        
        self.logging.basicConfig(filename=self._path_logger+self._helper.getSerialNow()+".log", level=logging.DEBUG )
        self.logging.Formatter(fmt='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        self.level              = level
        
        self.logging.info(self._helper.getTimeNow()+" Application -> "+self._app_name+" started in  "+platform.platform()+" with processor "+platform.processor())
    
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