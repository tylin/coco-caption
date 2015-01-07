#!/usr/bin/env python
# 
# File Name : convert_txt_to_json.py
#
# Description :
#
# Usage :
#
# Creation Date : 05-01-2015
# Last Modified : Mon Jan  5 17:46:07 2015
# Author : Hao Fang


import os
import sys
import argparse
import json

pa = argparse.ArgumentParser(
        description='convert caption in txt to json')
pa.add_argument('image_id_file', \
        type=argparse.FileType('r'), \
        help='image id file')
pa.add_argument('caption_txt_file', \
        type=argparse.FileType('r'), \
        help='caption file in txt format')
pa.add_argument('ncap_per_image', type=int, \
        help='number of captions per image')
pa.add_argument('json_file', \
        type=argparse.FileType('w'), \
        help='output json file')
args = pa.parse_args()

ids = [ line.rstrip() for line in args.image_id_file ]

json_data = {}
for image_id in ids:
    if image_id in json_data:
        print >> sys.stderr, 'Error: Multiply defined', image_id
    json_data[image_id] = []
    for i in xrange(args.ncap_per_image):
        line = args.caption_txt_file.readline().rstrip()
        assert(line != '')
        json_data[image_id].append(line)

assert(args.caption_txt_file.readline() == '')

json.dump(json_data, args.json_file)
