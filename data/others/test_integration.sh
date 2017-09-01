#!/bin/bash

echo "Testing Crawler..."

cd ../../applications/crawler/

python Main.py --mode crawler --dataset graffiti --classes graffiti,street --num_images 10 --flickr_tags graffiti,street


echo "Testing Compiler..."

cd ../compiler/

python Main.py --dataset_name graffiti --subset_name graffiti_per70_porp_80 --per_images 70 --train_proportional_size 80

