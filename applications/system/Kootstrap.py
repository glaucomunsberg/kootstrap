import json, traceback, os

class Kootstrap:
    
    _instance   = None
    
    config      = None
    flickr      = None
    scissor     = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Helper, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        
        path = os.path.abspath(".")
        path = path.split("/")
        path = path[:-2]
        absolute_path = ""
        for pat in path:
            absolute_path+=pat+"/"        
            
        try:
            with open('../../data/configs/kootstrap.json', 'r') as f:   
                self.config = json.load(f)    
        except:
            print "ERROR to load kootstrap.json"
            print traceback.format_exc()
            return
        
        if absolute_path != self.config['path_root']:
            self.config['path_root'] = absolute_path
            try:
                with open('../../data/configs/kootstrap.json', 'w') as f:   
                    json.dump(self.config, f)
            except:
                print "ERROR to update config absolute path"
                print traceback.format_exc()
        
        try:
            with open(self.config['path_root']+self.config['path_config']+'flickr.json', 'r') as f:   
                self.flickr = json.load(f)
        except:
            print "ERROR to load flickr.json"
            print traceback.format_exc()
            
        try:
            with open(self.config['path_root']+self.config['path_config']+'scissor.json', 'r') as f:   
                self.scissor = json.load(f)
        except:
            print "ERROR to load flickr.json"
            print traceback.format_exc()
            
        try:
            with open(self.config['path_root']+self.config['path_config']+'trainer.json', 'r') as f:   
                self.trainer = json.load(f)
        except:
            print "ERROR to load trainer.json"
            print traceback.format_exc()
    
    def path_config(self):
        return self.config['path_root']+self.config['path_config']
    
    def path_test(self):
        return self.config['path_root']+self.config['path_test']
    
    def path_log(self):
        return self.config['path_root']+self.config['path_log']
    
    def path_model(self):
        return self.config['path_root']+self.config['path_model']
    
    def path_dataset(self):
        return self.config['path_root']+self.config['path_dataset']
    
    def version(self):
        return self.config['version']