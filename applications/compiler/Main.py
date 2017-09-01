#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from Compiler import Compiler

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--dataset_name',type=str, default="dataset_example", help='name of dataset selected.')
    parser.add_argument('--subset_name',type=str, default=None, help='name of subset. If not passed will setted as <dataset_name>_<serial_data>')
    parser.add_argument('--classes', type=str, default=None,help='if empty and --classes_load_file empty the Compiler use all classes inside the dataset. Separete classes wite comma.')
    parser.add_argument('--classes_load_file', type=str, default=None,help='If not empty load form file the name of classes')
    parser.add_argument('--num_images', type=int, default=-1, help='Number of images from dataset. If negative use --per_images else both negative use all images.')
    parser.add_argument('--per_images', type=int, default=-1, help='percent of images from dataset [-1,100]. If negative use --num_images else both negative use all images')
    parser.add_argument('--scissor', type=str, default="yes", help='if scissor is on will cut images has configs scissor.json else keep the image on exactly same size (only copy)')
    parser.add_argument('--test_set', type=str, default="yes")
    parser.add_argument('--train_set', type=str, default="yes")
    parser.add_argument('--train_proportional_size', type=int, default=70,help='size of train, default 70%, setted if test exists')
    parser.add_argument('--annotation', type=str, default="",help='text annotation used you to describe the dataset')
    
    Annotation
    args = parser.parse_args()

    mode = Compiler(args)
    mode.start()

if __name__ == '__main__':
    main()