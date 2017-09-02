# Compiler

The compiler help you to create a dataset and subsets used to train or test. Try execute the `Main.py` class.

## Commands 

Start to create a dataset with two classes.
    
    python Main.py --mode dataset --dataset_name graffiti --classes graffiti,street
    
    
Create a subset of this dataset with 90% original images

    python Main.py --mode compiler  --dataset_name graffiti --subset_name graffiti_per90_porp_default --per_images 90

#### Arguments

* **--mode**: Use `dataset` to create a new and `compiler` to subsets.

* **--dataset_name**: Name used to dataset. Default `dataset_example`.

* **--classes_load_file**: If not empty load form file the name of classes.

* **--classes**: if empty and --classes_load_file empty the Compiler use all classes inside the dataset. Separete classes wite comma.


* **--subset_name**: name of subset. If not passed will setted as `<dataset_name>_<serial_data>`.

* **--num_images**: Number of images from dataset. If negative use --per_images else both negative use all images.

* **--per_images**: percent of images from dataset [-1,100]. If negative use --num_images else both negative use all images.

* **--scissor**: if scissor is on will cut images has configs scissor.json else keep the image on exactly same size (only copy).

* **--train_proportional_size**: size of train, default 70%, setted if test exists.

* **--validation_proportional_size**: size of validation, default 20%, setted if validation exists. Zero if dont want validation

* **--test_proportional_size**: size of validation, default 20%, setted if test exists. Zero if dont want test 

* **--annotation**: text annotation used you to describe the subset.

