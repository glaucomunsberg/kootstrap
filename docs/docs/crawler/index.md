# Welcome to Crawler

A set of programs that help you create a dataset and crawls in dataset information to compile the classes of your dataset

## Commands

Start executing to create a dataset with two classes.
    
    python Main.py --mode [crawler,dataset] --dataset dataset_example --classes graffiti,street --flickr_tags graffiti;tags
    
    
#### Arguments

* **--mode**: Choose de dataset to use in clawer, if no exist will be created. `"dataset"` if you want only create a dataset and her classes. `"crawler"` if you create and crawls the classes images from the `crawler_mode`.

* **--dataset_name**: Name used to dataset. Default `dataset_example`

* **--classes**: List of classes to create into dataset. Separated by comma

* **--classes_load_file**: load name of classes by file, one class by line or separated by ; if .csv. try something like the file `data/others/classes_name_imagenet.txt`

* **--clawler_mode**: The source of images. Default `"flickr"`.

* **--flickr_tags**: Name of tags useds on flickr, use comma to sum tags on search and (;) to separate de group of tags by classes. The same order of `--classes` need by used in `--flickr_tags`

* **--num_images**: Total image per class. Default `100`