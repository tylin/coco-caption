#!/usr/bin/env python
# 
# File Name : preprocess.py
#
# Description :
#
# Usage :
#
# Creation Date : 02-01-2015
# Last Modified : Mon Jan  5 17:50:53 2015
# Author : Hao Fang

import sys
from tokenizer.ptbtokenizer import PTBTokenizer
import multiprocessing

def tokenize(id_captions):
    """Tokenize the captions for an image.

    Args:
        id_captions: a tuple of (id, [captions])

    Returns:
        a tuple of (id, [tokenized_captions]).
    """
    id = id_captions[0]
    print >> sys.stderr, "Tokenizing", id
    tokenized_captions = []
    tokenizer = PTBTokenizer()
    for s in id_captions[1]:
        tokenized_captions.append(tokenizer.tokenize(s))

    return (id, tokenized_captions)

def tokenize_captions(obj, nthreads = 1):
    """Tokenize the captions for all images in the json object.

    Args:
        obj: (id, [captions]) pairs in json format. Values are a list of
        captions.
        nthreads: number of threads, default 1.

    Returns:
        (image_id, [tokenized_captions]) in json format. Values are a list of
        tokenized (and lower-cased) captions.
    """
    pool = multiprocessing.Pool(processes = nthreads)
    #tokenized_captions = pool.map(tokenize, obj.items())
    tokenized_captions = []
    for k, v in obj.items():
        tokenized_captions.append(tokenize((k, v)))
    return dict(tokenized_captions)
