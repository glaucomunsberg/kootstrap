# Definition

`Crawler.py` is a class that compile informations to `Dataset.py` and use the `Flickr.py` do crawls informations inside each of classes.

## Params

**args**: Args. `type:argparse`

**logger**: logger used in application default value is None. `type:Logger`

## Attributes

**dataset** : Return the name of dataset.`type:Dataset` 

**tags_by_class** : List of tags by class `type:List`

**num_images**: Number of images by class `type:Int`

**crawler_md**: Object crawler_md `type:Metadata`