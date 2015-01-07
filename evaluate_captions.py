#!/usr/bin/env python
# 
# File Name : evaluate_captions.py
#
# Description :
#
# Usage :
#
# Creation Date : 06-01-2015
# Last Modified : Tue Jan  6 16:54:20 2015
# Author : Hao Fang

import os

path_to_tokenized_ref_txt = 'data/debug.tokenized_ref.txt'
path_to_raw_hypo_txt = 'data/debug.hypo.txt'
num_refs_per_hypo = int(4)

path_to_tokenized_hypo_txt = 'var/tokenized_hypo.txt'

from caption_eval.evals import PTBTokenizer, Bleu, Rouge, Meteor, Cider

# =================================================
# Tokenize hypotheses
# =================================================
print 'tokenizing hypothese...'
tokenizer = PTBTokenizer()
token_lines = tokenizer.tokenize(open(path_to_raw_hypo_txt))
outfile = open(path_to_tokenized_hypo_txt, 'w')
for line in token_lines:
    outfile.write(line + '\n')
outfile.close()
print 'all hypothese have been tokenized'

# =================================================
# Compute Bleu (up to 4-gram)
# - using 'shortest' reference length as brevity penalty
# Also provides n-gram precision w/o brevity penalty (This is NOT Bleu)
# =================================================
scorer = Bleu()
score, bleu_info = scorer.compute_score(open(path_to_tokenized_hypo_txt), \
        open(path_to_tokenized_ref_txt), \
        num_refs_per_hypo)
print 'Bleu: ', score
print 'Bleu info: ', bleu_info

# =================================================
# Compute Meteor
# =================================================
scorer = Meteor()
score = scorer.compute_score(open(path_to_tokenized_hypo_txt), \
        open(path_to_tokenized_ref_txt), \
        num_refs_per_hypo)
print 'Meteor: ', score
