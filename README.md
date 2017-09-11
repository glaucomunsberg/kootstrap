![Build Status](http://glaucomunsberg.com/wp-content/uploads/2017/09/kootstrap.png)

**Kootstrap** is a *bootstrap* to [Keras](https://keras.io/). It is a technique of compile and loading a datasets into a Keras application by means of a few initial instructions that enable the introduction of the rest of the program from an input device.

[![Build Status](https://travis-ci.org/glaucomunsberg/kootstrap.svg?branch=master)](https://travis-ci.org/glaucomunsberg/kootstrap)

## Commands 

**Create a dataset** with two classes.

    cd maker/
    python Main.py --mode dataset --dataset_name graffiti --classes graffiti,street
    
    
**Create a subset** of this dataset with 90% original images
    
    python Main.py --mode compiler  --dataset_name graffiti --subset_name graffiti_per90_porp_default --per_images 90

**Crawls images** to each class from Flickr. This seed the dataset and compile the subsets.
    
    cd ../crawler/
    python Main.py --mode crawler,dataset --dataset dataset_example --classes graffiti,street --flickr_tags graffiti,street\ art;street --num_images 100
    
**Execute a train** with finetuning in Imagenet Model

    cd ../trainer/
    python Main.py --model_name model_example_1 --load_data dataset_example
    
**Test the predictions** on model with set of test compileted in `graffiti_per90_porp_default`

    cd ../tester/
    python Main.py --model_name model_example_1 --load_data graffiti_per90_porp_default

**Compile a 1-Top** with a histogram from test results:

	cd ../analyzer/
	python Main.py --model_name top --test_name testing_imagenet_test_set
	
## Migrate datasets

if you have a dataset and want migrate try:

	cd ../tools/
	python Main.py --mode migrate --path_origin <PATH_FOLDER_WITH_CLASSES> --path_destiny <PATH_TO_KOOTSTRAP_FOLDER> 
	
if you want create a subset or recovery the `metadata.json` try:

	cd ../tools/
	python Main.py --mode fix --path_origin <PATH_TO_SUBSET_OR_DATASET>