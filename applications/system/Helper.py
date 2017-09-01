#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

class Helper:
    _instance   = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Helper, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        None
    
    def getSerialNow(self):
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    def getTimeNow(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def filePathToList(self,path_file):
        lines = []
        file = open(path_file,'r')
        for line in file:
            lines.append(line.replace('\n', '').replace('\r', ''))
        return lines