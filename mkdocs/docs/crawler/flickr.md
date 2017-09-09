# Definition

`Flickr.py` is a final class used by `Crawler.py` to download images from Flickr to a dataset created or open by `Dataset.py`.

## Params

**args**: Args. `type:argparse`

**crawler_md**: the crawler metadata references. `type:Metadata`

**class_name**: name of class inside of dataset to put all files crawled.

**tags**: the tags used to crawls of the param `class_name`.

**num_img_to_download**: Number of images to crawled of this `tags`.

**year**: Year of photo on flickr.

**month**: Month of photo on flickr.

**day**: Day of photo on flickr.

**logger**: logger used in application default value is None. `type:Logger`

## Attributes

**images_metadata** : List of images and their informations.`type:List` 
 
    `[{'flickr_id':'91719271212', 'width':500,'height':500,'visible':true,'name':'91719271212_ah1cde.jpg'}]`

**total_images** : Number of images download of tags by class `type:List`.

**num_img_to_download**: Number of images that need by downloaded.