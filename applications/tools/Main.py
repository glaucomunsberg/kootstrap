#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MigrateDataset import MigrateDataset
from FixMetadata import FixMetadata
from Transfer import Transfer
import argparse

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--mode', type=str, default='migrate', help="Use the mode 'migrate','fix' or 'transfer'")
    parser.add_argument('--path_origin', type=str, default=None, help='relative path or absolute path from origin files')
    parser.add_argument('--path_destiny', type=str, default=None, help='relative path or absolute path to destiny files.')
    parser.add_argument('--copy_way', type=str, default=None, help="'copy' or 'move' if empty choose from kootstrap configuration")
    parser.add_argument('--max_files_by_class', type=int, default=-1, help="if negative move all and 0 no one")
    
    args = parser.parse_args()

    if args.mode == "migrate":
        mode = MigrateDataset(args)
        mode.start()
    elif args.mode == "fix":
        mode = FixMetadata(args)
    else:
        mode = Transfer(args)
        mode.start()

if __name__ == '__main__':
    main()