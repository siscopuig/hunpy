#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
Convenience wrapper for running hunpy directly from source tree.
"""

from hunpy.hunpy import main

config_yml_file_path = ['config/hunpy.yml']

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Hunpy')
    parser.add_argument('-u', '--url', help='url to process', action='append')
    parser.add_argument('-a', '--headless', help='runs browser in headless mode', action='store_true')
    parser.add_argument('-d', '--debug', help='show verbose', action='store_true')
    args = parser.parse_args()

    main(args, config_yml_file_path)