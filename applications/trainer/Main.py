#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Trainer import Trainer
import argparse

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--model_name', type=str, default=None, help='Set the name of this model train or use --load_model')
    parser.add_argument('--load_model_file', type=str, default=None, help='Choose a particular model from a .json file')
    
    parser.add_argument('--load_data', type=str, default=None, help='Path to any subset or dataset compiled by koopstrap. try only the name of set too.')
    
    parser.add_argument('--load_weights', type=str, default=None, help='Location to pretrained model')
    
    parser.add_argument('--annotation', type=str, default=None, help='text annotation used you to describe the model')
    
    args = parser.parse_args()

    trainer = Trainer(args) 
    
    trainer.start()

if __name__ == '__main__':
    main()