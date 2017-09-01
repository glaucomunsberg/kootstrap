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
