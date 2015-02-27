#!/usr/bin/env python
# 
# File Name : tokenize_ref.py
#
# Description :
#
# Usage :
#
# Creation Date : 25-02-2015
# Last Modified : Wed Feb 25 13:20:19 2015
# Author : Hao Fang

path_to_raw_ref_json = 'data/val_captions_coco2014_ref.json'
path_to_tokenized_ref_json = 'data/val_captions_coco2014_ref.tokenized.json'

from caption_eval.tokenizer.ptbtokenizer import PTBTokenizer

# =================================================
# Load references
# =================================================
import json
raw_ref_for_image = json.load(open(path_to_raw_ref_json))

# =================================================
# Tokenize references
# =================================================
print 'tokenizing', len(raw_ref_for_image), 'references ...' 
tokenizer = PTBTokenizer()
tokenized_ref_for_image= tokenizer.tokenize(raw_ref_for_image)
keys1 = raw_ref_for_image.keys() 
keys1.sort()
keys2 = tokenized_ref_for_image.keys()
keys2.sort()
assert(keys1 == keys2)
print 'all references have been tokenized'

json.dump(tokenized_ref_for_image, open(path_to_tokenized_ref_json, 'w'))
