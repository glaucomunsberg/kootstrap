# Kootstrap
Kootstrap is a bootstrap to Keras. It is a technique of compile and loading a datasets into a Keras application by means of a few initial instructions that enable the introduction of the rest of the program from an input device.

[![Build Status](https://travis-ci.org/glaucomunsberg/kootstrap.svg?branch=master)](https://travis-ci.org/glaucomunsberg/kootstrap)

## Commands 

Start to create a dataset with two classes.

    cd maker/
    python Main.py --mode dataset --dataset_name graffiti --classes graffiti,street
    
    
Create a subset of this dataset with 90% original images
    
    python Main.py --mode compiler  --dataset_name graffiti --subset_name graffiti_per90_porp_default --per_images 90

Crawls 100 images for each class from flickr. This seed the dataset and compile the subsets.
    
    cd ../crawler/
    python Main.py --mode crawler,dataset --dataset dataset_example --classes graffiti,street --flickr_tags graffiti,street\ art;street --num_images 100
    
Execute a train with finetuning in Imagenet Model

    cd ../trainer/
    python Main.py --model_name model_example_1 --load_data dataset_example
    
Test the predictions on model with set of test compileted in `graffiti_per90_porp_default`

    cd ../tester/
    python Main.py --model_name model_example_1 --load_data graffiti_per90_porp_default
