#!/bin/bash

echo "Testing a dataset..."

cd ../../applications/maker/

python Main.py --mode dataset --dataset_name graffiti --classes graffiti,street

python Main.py --mode dataset --dataset_name imagenet --classes_load_file ../../data/others/imagenet_classes.txt 

echo "Testing compile a subset..."

python Main.py --mode compiler  --dataset_name graffiti --subset_name graffiti_per90_porp_default --per_images 90

echo "Testing crawler..."

cd ../../applications/crawler/

python Main.py --dataset_name graffiti --classes graffiti,street --num_images 10 --flickr_tags graffiti,street

echo "Testing Training..."

cd ../trainer/

#python Main.py --load_subset ../../data/datasets/graffiti/subsets/graffiti_per70_porp_80/ 