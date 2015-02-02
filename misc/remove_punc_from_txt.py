#!/usr/bin/env python
# 
# File Name : remove_punc_from_txt.py
#
# Description :
#
# Usage :
#
# Creation Date : 02-02-2015
# Last Modified : Mon Feb  2 11:59:12 2015
# Author : Hao Fang

import os
import sys
import argparse

PUNCTUATIONS = ["''", "'", "``", "`", "-LRB-", "-RRB-", "-LCB-", "-RCB-", \
        ".", "?", "!", ",", ":", "-", "--", "...", ";"]

pa = argparse.ArgumentParser(
        description='remove puncutation from the txt file')
pa.add_argument('orig_txt', \
        type=argparse.FileType('r'), \
        help='original txt file (already tokenized)')
args = pa.parse_args()

for line in args.orig_txt:
    units = line.rstrip().split(' ')
    print ' '.join(w for w in units if w not in PUNCTUATIONS)
