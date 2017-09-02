#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from Compiler import Compiler
from Dataset import Dataset

def main():
    parser = argparse.ArgumentParser()
    
    # dataset
    parser.add_argument('--mode',type=str, default="", help='try the mode dataset or compiler (to subset)')
    parser.add_argument('--dataset_name',type=str, default="dataset_example", help='name of dataset selected.')
    parser.add_argument('--classes_load_file',type=str, default=None, help='load names of classes if you can a long list of complex names')
    parser.add_argument('--classes',type=str, default=None, help='name of classes that you want in dataset. Separated by comma. None load all classes from dataset')
    # compiler
    parser.add_argument('--subset_name',type=str, default=None, help='name of subset. If not passed will setted as <dataset_name>_<serial_data>')
    parser.add_argument('--num_images', type=int, default=-1, help='Number of images by classe. If negative use all images from classe.')
    parser.add_argument('--per_images', type=int, default=100, help='percent of images from dataset [-1,100]. If negative use --num_images else both negative use all images')
    parser.add_argument('--scissor', type=str, default="yes", help='if scissor is on will cut images has configs scissor.json else keep the image on exactly same size (only copy)')
    parser.add_argument('--train_proportional_size', type=int, default=60,help='size of train, default 70%, setted if test exists')
    parser.add_argument('--validation_proportional_size', type=int, default=20,help='size of validation, default 20%, setted if test exists. Zero if dont want validation')
    parser.add_argument('--test_proportional_size', type=int, default=20,help='size of train, default 20%, setted if test exists')
    parser.add_argument('--annotation', type=str, default="",help='text annotation used you to describe the dataset')
    
    args = parser.parse_args()
    
    mode = None
    if args.mode == "dataset":
        mode = Dataset(args)
    else:
        mode = Compiler(args)
    mode.start()

if __name__ == '__main__':
    main()