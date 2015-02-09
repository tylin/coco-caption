# Filename: preprocessing_cider.py
#
# Description: Script to perform the preprocessing on references for computing the CIDEr metric
#
# Author: Ramakrishna Vedantam
#
# Notes: Saves "dictionary.pickle" , "references.pickle" files 
#
# Date Created: Sun Feb  8 20:50:07 2015

from cider import *
import json
import numpy as np
import pdb
import scipy.io as si
import pickle

# load the already tokenized reference sentences
path_to_tokenized_ref_json = '../../data/tokenized_ref.nopunc.json'
ref = json.load(open(path_to_tokenized_ref_json))

# split the sentences into lists of str
split_tokens(ref)
# TO-DO implement stemming

# Get the n-gram dictionary
all_refs = ref.values()
conc_refs = concatenate(all_refs)
# set ngrams = 4 for CIDEr
words = index_words(conc_refs, ngrams= 4)
# obtain IDF values
idf = compute_idf(words, ref, ngrams=4)
# save the data 
pickle.dump(words, open('../../data/words_ref.p','w'));
pickle.dump(idf, open('../../data/idf_ref.p','w'));

# project reference sentences into the n-gram vector space
ref_vecs = ngrams_to_vectors(ref, words, ngrams=4)
pickle.dump(ref_vecs, open('../../data/ref_vecs.p','w'));
