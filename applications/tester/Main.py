#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tester import Tester
import argparse

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--model_name', type=str, default=None, help='Set the name of this model to test')
    parser.add_argument('--load_data', type=str, default=None, help='Path to any subset or dataset compiled by kootstrap to test, if None we use the test set from subset of train')
    parser.add_argument('--test_name', type=str, default=None, help='Name to this test, if empty save a composition from serial number and the dataset tested')
    parser.add_argument('--epoch', type=int, default=-1, help='Set the epoch with weigths that you want save')
    parser.add_argument('--set', type=str, default='test', help='Choose if the test will use the train, validation or test set of images on subset else selected a dateset the arg will by ignorated')
    parser.add_argument('--annotation', type=str, default="", help='Annotation about test')
    
    args = parser.parse_args()
    
    tester = Tester(args)
    tester.start()

if __name__ == '__main__':
    main()