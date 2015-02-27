#!/usr/bin/env python
# 
# File Name : convert_json_to_txt_id.py
#
# Description :
#
# Usage :
#
# Creation Date : 25-02-2015
# Last Modified : Wed Feb 25 12:49:16 2015
# Author : Hao Fang

import os
import sys
import argparse
import json

pa = argparse.ArgumentParser(
        description='convert json to txt and the id list')
pa.add_argument('json_file', \
        type=argparse.FileType('r'), \
        help='json file')
pa.add_argument('output_txt_file', \
        type=argparse.FileType('w'), \
        help='output txt file')
pa.add_argument('output_id_file', \
        type=argparse.FileType('w'), \
        help='output id file')
args = pa.parse_args()

json_data = json.load(args.json_file)
for k, v in json_data.iteritems():
    assert(type(v) is list)
    for c in v:
        for sentence in c.splitlines():
            args.output_id_file.write(k + '\n')
            args.output_txt_file.write(sentence + '\n')

