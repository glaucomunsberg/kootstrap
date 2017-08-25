#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse,sys

sys.path.append('../')

from system.Koopstrap import Koopstrap
from system.Metadata import Metadata
from system.Logger import Logger
from system.Helper import Helper
from Dataset import Dataset

class Crawler:
    
    _koopstrap      = None
    _logger         = None
    _helper         = None
    _args           = None
    
    dataset         = None
    
    def __init__(self,args):
        
        self._koopstrap = Koopstrap()
        self._logger    = Logger(app_name='Crawler')
        self._helper    = Helper()
        self._args      = args
        self.dataset    = Dataset(args) 
        
    def start(self):
        self.dataset.start()
        None
        