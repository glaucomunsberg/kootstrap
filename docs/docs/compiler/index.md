# Compiler

The compiler help you to manipulate a dataset to create subsets used in train or test. Try execute the `Main.py` class.

## Commands 

Start to create a subset with 70% of original size and 80% of train and 20% to test.
    
    python Main.py --dataset_name graffiti --subset_name graffiti_per70_porp_80 --per_images 70 --train_proportional_size 80

#### Arguments

* **--dataset_name**: Name used to dataset. Default `dataset_example`.

* **--subset_name**: name of subset. If not passed will setted as `<dataset_name>_<serial_data>`.

* **--classes**: if empty and --classes_load_file empty the Compiler use all classes inside the dataset. Separete classes wite comma.

* **--classes_load_file**: If not empty load form file the name of classes.

* **--num_images**: Number of images from dataset. If negative use --per_images else both negative use all images.

* **--per_images**: percent of images from dataset [-1,100]. If negative use --num_images else both negative use all images.

* **--scissor**: if scissor is on will cut images has configs scissor.json else keep the image on exactly same size (only copy).

* **--test_set**: if scissor is on will cut images has configs scissor.json else keep the image on exactly same size (only copy).

* **--train_proportional_size**: size of train, default 70%, setted if test exists

* **--annotation**: text annotation used you to describe the subset.

