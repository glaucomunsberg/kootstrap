# Welcome to Kootstrap

Kootstrap is a _bootstrap_ to [Keras](http://keras.io). It is a technique of compile and loading a datasets into a Keras application by means of a few initial instructions that enable the introduction of the rest of the program from an input device

## Get Code
    
If you want to get code or contribute, go to [Kootstrap GitHub](https://github.com/glaucomunsberg/kootstrap).


## Commands 


Bellow you find how [create a dataset](#create-a-dataset), [a subset](#create-a-subset), [crawls images](#crawls-images) and  [execute a trainig](#execute-a-training) your own model.


### Create a dataset

**Create a dataset** with two classes.

    cd maker/
    python Main.py --mode dataset --dataset_name graffiti --classes graffiti,street
    
    
### Create a subset

**Create a subset** of this dataset with 90% original images.
    
    python Main.py --mode compiler  --dataset_name graffiti --subset_name graffiti_per90_porp_default --per_images 90

### Crawls images

**Crawls images** to each class from Flickr. This seed the dataset and compile the subsets.
    
    cd ../crawler/
    python Main.py --mode crawler,dataset --dataset dataset_example --classes graffiti,street --flickr_tags graffiti,street --num_images 100
    
### Execute a training

**Execute a training** with finetuning in Imagenet Model.

    cd ../trainer/
    python Main.py --model_name model_example_1 --load_data dataset_example
    
### Test the predictions

**Test the predictions** on model with set of test compileted in `graffiti_per90_porp_default`.

    cd ../tester/
    python Main.py --model_name model_example_1 --load_data graffiti_per90_porp_default


### Compile a 1-Top charts

**Compile a 1-Top** with a histogram from test results.

	cd ../analyzer/
	python Main.py --model_name top --test_name testing_imagenet_test_set



## Tools


### Migrate datasets

if you have a dataset and want migrate try:

	cd ../tools/
	python Main.py --mode migrate --path_origin <PATH_FOLDER_WITH_CLASSES> --path_destiny <PATH_TO_KOOTSTRAP_FOLDER> 
	
if you want create a subset or recovery the `metadata.json` try:

	cd ../tools/
	python Main.py --mode fix --path_origin <PATH_TO_SUBSET_OR_DATASET>

## Project layout

    data/           # folder with all data generate by applications.
        configs/
        models/
        datasets/
        tests/
        others/
    applications/   # applications suches crawler, analyzers etc
        analyzer/
        crawler/
        maker/
        system/
        tester/
        tools/
        trainer/
    docs/           # documentation of kootstrap
    mkdocs/         # generator of documentation


## Graphium

Try use models trained on [Kootstrap](https://github.com/glaucomunsberg/kootstrap) on your [Graphium](https://github.com/glaucomunsberg/graphium) application.