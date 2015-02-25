#!/usr/bin/env python
# 
# File Name : convert_txt_id_to_json.py
#
# Description :
#
# Usage :
#
# Creation Date : 25-02-2015
# Last Modified : Wed Feb 25 12:47:34 2015
# Author : Hao Fang

import os
import sys
import argparse
import json
from collections import defaultdict

pa = argparse.ArgumentParser(
        description='convert txt and the id list to json')
pa.add_argument('txt_file', \
        type=argparse.FileType('r'), \
        help='txt file')
pa.add_argument('id_file', \
        type=argparse.FileType('r'), \
        help='id file')
pa.add_argument('json_file', \
        type=argparse.FileType('w'), \
        help='output json file')
args = pa.parse_args()

image_ids = [ line.rstrip() for line in args.id_file ]
captions = [ line.rstrip() for line in args.txt_file ]
assert len(image_ids) == len(captions)

json_data = defaultdict(list)
for i in xrange(len(image_ids)):
    json_data[image_ids[i]].append(captions[i])
json.dump(json_data, args.json_file)
