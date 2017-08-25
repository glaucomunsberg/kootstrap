#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from Crawler import Crawler
from Dataset import Dataset

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--mode',type=str, default="", help='try the mode crawler,dataset')
    parser.add_argument('--dataset_name',type=str, default="dataset_example", help='name of dataset selected. Final name you replace spaces into _.')
    parser.add_argument('--classes',type=str, default="class_1,class_2", help='name of classes that you want in dataset. Separated by comma')
    parser.add_argument('--classes_load_file',type=str, default=None, help='load names of classes if you can a long list of complex names')
    parser.add_argument('--clawler_mode',type=str, default="flickr", help='Source from information')
    parser.add_argument('--flickr_tags',type=str, default="graffiti;street", help='Tag to crawls the flickr. Use comma (,) if you want more that one tag to classe, use (;) of Separate the tag from class destiny')
    
    parser.add_argument('--num_images', type=int, default=100)
    args = parser.parse_args()

    mode = None
    
    if args.mode == "crawler":
        mode = Crawler(args)
    elif args.mode == "dataset":
        mode = Dataset(args)
    else:
        print 'Error: --mode '+args.mode+" not defined!"
        
    if mode != None:
        mode.start()

if __name__ == '__main__':
    main()