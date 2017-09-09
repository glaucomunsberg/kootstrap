#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from Analyzer import Analyzer

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--mode',type=str, default="top", help='select the top or visualization')
    parser.add_argument('--title', type=str, default='Kootstrap visualization', help='Name to plot')
    
    # Top params
    parser.add_argument('--number_of_tops',type=int, default=1, help='Number of classe to.')
    parser.add_argument('--test_name', type=str, default=None, help='Name from folder of test or path to')
    parser.add_argument('--save_histogram_to_csv', type=str, default='true', help='Generate the .csv file')
    parser.add_argument('--save_histogram_to_png', type=str, default='true', help='Plot the result in .png file')
    parser.add_argument('--save_list_image', type=str, default='true', help='Generate the .csv with label and images from tops')
    parser.add_argument('--number_limit_to_y', type=int, default=-1, help='Top in chat to y. -1 do default')
    
    # Visualization params
    parser.add_argument('--files',type=str, default=None, help='Select file or choose on executation. Multiples files need a comma to separate')
    parser.add_argument('--model_name',type=str,default=None, help='Set the name of this model to test')
    parser.add_argument('--modifier',type=str,default='None',help="you can choose None, 'guided', 'relu','deconv' and 'rectified'. separeted by comma if want multiple")
    parser.add_argument('--class_name', type=str, default=None, help='Name of classe used')
    parser.add_argument('--show_both', type=str, default="yes", help='show image and image with heatmap side by side')
    parser.add_argument('--epoch', type=int, default=-1, help='Set the epoch with weigths that you want save')
    args = parser.parse_args()
    
    mode = None
    if args.mode in ["top","visualization"]:
        mode = Analyzer(args)
    else:
        print 'Error: --mode '+args.mode+" not defined!" 
        
    if mode != None:  
        mode.start()

if __name__ == '__main__':
    main()