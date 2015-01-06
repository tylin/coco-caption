#!/usr/bin/env python

import os
import sys
import itertools
from caption_eval.evals import Bleu

verbose = 1
path_to_ref_file = 'misc/data_preparation/debug.tokenized_ref.txt'
path_to_hypo_file = 'misc/data_preparation/debug.tokenized_hypo.txt'

num_refs_per_hypo = 4
bleus = Bleu()

## STEP 0: READ IN TESTS
testlines = []
for line in open(path_to_hypo_file, 'r'):
    testlines.append(line.rstrip())

## STEP 1: READ IN REFS
refs = []
ref_file = open(path_to_ref_file, 'r')
for i, line in enumerate(ref_file):
    if i % num_refs_per_hypo == 0:
        refs.append([])
    refs[-1].append(line.rstrip())

## STEP 2: COOK TESTS
for i, (testline, ref) in enumerate(zip(testlines, refs), 1):
    bleus += (testline, ref)

## STEP 3: EVALUATE (with effective ref len)
bleu = bleus.compute_score(option='closest', verbose=verbose)
ratio = bleus.ratio()
print >> sys.stderr, \
        "bleu%s = %.4lf, length_ratio = %.2lf (%d sentences, length option \"%s\")" \
        % ("+1" if bleus.size() == 1 else "", bleu, ratio, bleus.size(), \
        'closest')

bleu = bleus.recompute_score(option='average', verbose=verbose)
ratio = bleus.ratio()
print >> sys.stderr, \
        "bleu%s = %.4lf, length_ratio = %.2lf (%d sentences, length option \"%s\")" \
        % ("+1" if bleus.size() == 1 else "", bleu, ratio, bleus.size(), \
        'average')

bleu = bleus.recompute_score(option='shortest', verbose=verbose)
ratio = bleus.ratio()
print >> sys.stderr, \
        "bleu%s = %.4lf, length_ratio = %.2lf (%d sentences, length option \"%s\")" \
        % ("+1" if bleus.size() == 1 else "", bleu, ratio, bleus.size(), \
        'shortest')
