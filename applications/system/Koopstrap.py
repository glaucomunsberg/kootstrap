import json, traceback

class Koopstrap:
    
    _instance   = None
    
    config      = None
    flickr      = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Helper, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        
        try:
            with open('../../data/configs/koopstrap.json', 'r') as f:   
                self.config = json.load(f)
        except:
            print "ERROR to load koopstrap.json"
            print traceback.format_exc()
            return
        
        try:
            with open(self.config['path_root']+self.config['path_config']+'flickr.json', 'r') as f:   
                self.cralwer = json.load(f)
        except:
            print "ERROR to load flickr.json"
            print traceback.format_exc()
        