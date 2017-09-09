#!/bin/bash

echo "Testing a dataset..."

cd ../../applications/maker/

python Main.py --mode dataset --dataset_name graffiti --classes graffiti,street

python Main.py --mode dataset --dataset_name imagenet --classes_load_file ../../data/others/imagenet_classes.txt 

echo "Testing compile a subset..."

python Main.py --mode compiler  --dataset_name graffiti --subset_name graffiti_per90_porp_default --per_images 90

python Main.py --mode compiler  --dataset_name imagenet --subset_name imagenet_per90_porp_default --per_images 90

echo "Testing crawler..."

cd ../crawler/

python Main.py --dataset_name graffiti --classes graffiti,street --num_images 10 --flickr_tags graffiti,street

python Main.py --dataset_name imagenet --classes bottlecap,bison --num_images 10 --flickr_tags bottlecap,bison
echo "Testing Training..."

cd ../trainer/

python Main.py --model_name model_example_1 --load_data imagenet_per90_porp_default

echo "Testing Testing..."

cd ../tester/

python Main.py --model_name model_example_1 --load_data imagenet_per90_porp_default

#python Main.py --model_name model_example_1 --load_data graffiti_per90_porp_default