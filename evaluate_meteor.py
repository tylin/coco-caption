#!/usr/bin/env python
# 
# File Name : evaluate_meteor.py


import os

path_to_tokenized_ref_json = 'data/tokenized_ref.nopunc.json'
path_to_raw_hypo_json = 'data/hypo.json'

from caption_eval.evals import PTBTokenizer, Bleu, Rouge, Meteor, Cider

# =================================================
# Load references
# =================================================
import json
tokenized_ref_for_image = json.load(open(path_to_tokenized_ref_json))

# =================================================
# Tokenize hypotheses
# =================================================
print 'tokenizing hypothesis...'
raw_hypo_for_image = json.load(open(path_to_raw_hypo_json))
tokenizer = PTBTokenizer()
tokenized_hypo_for_image= tokenizer.tokenize(raw_hypo_for_image)
keys1 = tokenized_hypo_for_image.keys() 
keys1.sort()
keys2 = tokenized_ref_for_image.keys()
keys2.sort()
assert(keys1 == keys2)
print 'all hypothesis have been tokenized'

# =================================================
# Compute Meteor
# =================================================
scorer = Meteor()
score = scorer.compute_score(tokenized_hypo_for_image, \
     tokenized_ref_for_image)
print 'Meteor: ', score


