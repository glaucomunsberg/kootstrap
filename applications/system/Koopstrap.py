import json, traceback

class Koopstrap:
    
    _instance   = None
    
    config      = None
    flickr      = None
    scissor     = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Helper, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        
        try:
            with open('../../data/configs/koopstrap.json', 'r') as f:   
                self.config = json.load(f)
        except:
            print "ERROR to load koopstrap.json at "
            print traceback.format_exc()
            return
        
        try:
            with open(self.config['path_root']+self.config['path_config']+'flickr.json', 'r') as f:   
                self.flickr = json.load(f)
        except:
            print "ERROR to load flickr.json at "+self.config['path_root']+self.config['path_config']
            print traceback.format_exc()
            
        try:
            with open(self.config['path_root']+self.config['path_config']+'scissor.json', 'r') as f:   
                self.scissor = json.load(f)
        except:
            print "ERROR to load flickr.json"
            print traceback.format_exc()
    
    def path_config(self):
        return self.config['path_root']+self.config['path_config']
    
    def path_log(self):
        return self.config['path_root']+self.config['path_config']
    
    def path_dataset(self):
        return self.config['path_root']+self.config['path_dataset']
    
    def version(self):
        return self.config['version']