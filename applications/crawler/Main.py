#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from Crawler import Crawler

def main():
    parser = argparse.ArgumentParser()
    
    # Crawler
    parser.add_argument('--mode',type=str, default="flickr", help='Source from information')
    parser.add_argument('--dataset_name',type=str, default="dataset_example", help='name of dataset selected to receive informations')
    parser.add_argument('--classes_load_file',type=str, default=None, help='load names of classes if you can a long list of complex names. Empty to load from --classes.')
    parser.add_argument('--classes',type=str, default=None, help='name of classes that you want in crawle information. empty all from dataset metadata.')
    parser.add_argument('--num_images', type=int, default=100)
    parser.add_argument('--feed_subsets', type=str, default="yes",help='if yes and have subsets the images crawled will splited inside of them')
    parser.add_argument('--annotation', type=str, default="",help='text annotation used you to describe the subset')

    # Flickr
    parser.add_argument('--flickr_tags_load_file',type=str, default=None, help='load name of tags by file, tags by line or separated by coma. try something like the file. Use comma to separate and newline to new class.')
    parser.add_argument('--flickr_tags',type=str, default="graffiti,street", help='Tag to crawls the flickr. Use comma separate the tag from class destiny. Multiple tags by class use --flickr_tags_load_file ')
    
    args = parser.parse_args()
    
    mode = Crawler(args)
    mode.start()

if __name__ == '__main__':
    main()