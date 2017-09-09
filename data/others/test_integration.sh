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

python Main.py --model_name model_example_1 --load_data imagenet_per90_porp_default --epochs 2

echo "Testing Testing..."

cd ../tester/

python Main.py --model_name model_example_1 --load_data imagenet_per90_porp_default --test_name testing_imagenet_test_set

#python Main.py --model_name model_example_1 --load_data graffiti_per90_porp_default

echo "Testing Analyzer..."

cd ../analyzer/

echo "Testing Analyzer: 1-Top..."

python Main.py --mode top --test_name testing_imagenet_test_set

echo "Testing Analyzer: Deep visualization..."

python Main.py --mode visualization --files ../../data/datasets/graffiti/classes/graffiti/4235365635_a5fba2a2d8_o.jpg --model_name model_example_1 --class_name freight\ car