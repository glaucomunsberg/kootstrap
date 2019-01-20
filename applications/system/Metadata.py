#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback, json

class Metadata:
    
    metadata = None
    path_file = None

    def __init__(self, path_file, create_file=False):

        self.path_file = path_file
        
        if create_file:
            self.metadata = {}
            try:
                with open(self.path_file, 'w') as f:   
                    json.dump(self.metadata, f)
            except:
                print "ERROR to create "+self.path_file
                print traceback.format_exc()
        else:
            try:
                with open(path_file, 'r') as f:   
                    self.metadata = json.load(f)
            except:
                print "ERROR to load "+self.path_file
                print traceback.format_exc()
        
    def save(self):
        try:
            with open(self.path_file, 'w') as f:   
                json.dump(self.metadata, f)
        except:
            print "ERROR to save "+self.path_file
            print traceback.format_exc()