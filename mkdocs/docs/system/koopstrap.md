# Definition

The koopstrap return a instance of Koopstrap. It is a Dic with many configs what you can see inside the directory `data/configs/`

## Attributes

**config** : the metadata of configuration has default. The file `data/configs/kooperstrap.json` is load to system.`type:Dic`

Keys inside attribute config:

    {
        "path_root": "<PATH>/kootstrap/",
        "path_log":"data/logs/",
        "path_config":"data/configs/",
        "path_dataset":"data/datasets/",
        "path_model": "data/models/",
        "path_test": "data/tests/",
        
        "file_exist_count_has_download":true,
        "transfer_file_type": "copy",
        "file_order_randomly": true,
        
        "log_level":"INFO",
        "version":"0.0.1"
    }
    
**flickr** : the metatada of flickr used has default. The file `data/configs/flickr.json` is load to system. `type:Dic`

Keys inside attribute flickr:

    {
        "flickr_public_key":"<YOUR_KEY>",
        "flickr_private_key":"<YOUR_PRIVATE_KEY>",
        "flickr_per_page":500,
        "flickr_year_min":2010,
        "flickr_year_max":2017,
        "flickr_size":"larger",
        "flickr_size_minimum":244,
        "flickr_size_maximum":800,
        "safe_mode":true
    }
    
**flickr** : the metatada of flickr used has default. The file `data/configs/flickr.json` is load to system. `type:Dic`

Keys inside attribute flickr:

    {
        "flickr_public_key":"<YOUR_KEY>",
        "flickr_private_key":"<YOUR_PRIVATE_KEY>",
        "flickr_per_page":500,
        "flickr_year_min":2010,
        "flickr_year_max":2017,
        "flickr_size_minimum_width":500,
        "flickr_size_minimum_height":500,
        "flickr_size_maximum_width":1024,
        "flickr_size_maximum_height":1024,
        "safe_mode":true
    }
    
**scissor** : the metatada of scissor used has default. The file `data/configs/scissor.json` is load to system. `type:Dic`

Keys inside attribute scissor:

    {
        "target_max_width":224,
        "target_max_height":224,
        "target_min_width":224,
        "target_min_height":224,
        "target_rate":0.8
    }

**trainer** : the metatada of trainer used has default. The file `data/configs/trainer.json` is load to system. `type:Dic`

Keys inside attribute scissor:

    {
        "model": "VGG16",
        "include_top": true,
        "weights": "imagenet",
        "batch_size": 128,
        "target_size": 224,
        "epochs_total": 2,
        "target_loss":-1.0,
        "target_acc":-1.0,
        "save_weights_to_each":2,
        "shuffle":true
    }

## Methods

**path_config**: Return absolute path to configurations of koopstrap. `type:String`

**path_test**: Return absolute path to tests folder. `type:String`

**path_log**: Return absolute path to logs of system. `type:String`

**path_model**: Return absolute path to models folder. `type:String`

**path_dataset**: Return absolute path to all datasets. `type:String`

**version**: Return version of koopstrap. `type:String`