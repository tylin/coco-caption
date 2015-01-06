#!/usr/bin/env python
# 
# File Name : tokenize_captions.py
#
# Description : Tokenize captions in json format.
#
# Usage :
#
# Creation Date : 02-01-2015
# Last Modified : Mon Jan  5 17:50:30 2015
# Author : Hao Fang

import os
import sys
import argparse
import json
import caption_eval.preprocess as preprocess


pa = argparse.ArgumentParser(
        description='tokenize the reference captions in json format')
pa.add_argument('json_file', type=argparse.FileType('r'), \
        help='image captions in json format')
pa.add_argument('--nthreads', type=int, default=1, help='number of threads')
pa.add_argument('out_json_file', type=argparse.FileType('w'), \
        help='output json file for tokenized captions')
args = pa.parse_args()

raw_captions = json.load(args.json_file)
tokenized_captions = preprocess.tokenize_captions(raw_captions, args.nthreads)

json.dump(tokenized_captions, args.out_json_file)
