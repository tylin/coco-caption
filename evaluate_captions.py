#!/usr/bin/env python

__author__ = 'tylin'

num_threads = 5
path_to_tokenized_ref_file = 'misc/debug.tokenized_ref.json'
path_to_raw_hypo_file = 'misc/debug.hypo.json'

from caption_eval.evals import Bleu, Rouge, Meteor, Cider
import caption_eval.preprocess as preprocess

# =================================================
# Load Data from JSON file
# The data is pairs of key(image_id) and value(caption(s))
# refs is reference captions
#
# =================================================
import json
print 'loading tokenized references...'
tokenized_refs = json.load(open(path_to_tokenized_ref_file, 'r'))

print 'loading raw hypotheses...'
raw_hypos = json.load(open(path_to_raw_hypo_file, 'r'))


# =================================================
# Preprocessing Data
# INPUT: list of captions
#        for testing captions, it is an array of object with key (image id) and value (list of captions).
# OUTPUT: normalized captions in python object with key (image id) and value (list of words)
# =================================================
print 'tokenizing hypothese, process %d captions...'%(len(raw_hypos))
tokenized_hypos = preprocess.tokenize_captions(raw_hypos, num_threads)
print 'all captions have been tokenized'

# =================================================
# Evaluation
# INPUT: pair of preprocessed tests and refs data
# OUTPUT: single value score
# All the evaluation methods are defined in class
# The class shares three member functions
#   score = eval.compute_score(tests, refs)
#       compute score given the test and ref data
#   method = eval.method()
#       show name of eval method
# =================================================
#evals = [Bleu(),
#         Meteor(),
#         Rouge(),
#         Cider()]
evals = [Bleu()]
for eval in evals:
    s = eval.compute_score(tokenized_hypos, tokenized_refs)
    print "%s score: %0.2f"%(eval.method(), s)
