#!/usr/bin/env python
# 
# File Name : ptbtokenizer.py
#
# Description : Do the PTB Tokenization and remove punctuations.
#
# Usage :
#
# Creation Date : 29-12-2014
# Last Modified : Mon Feb  2 11:51:12 2015
# Author : Hao Fang

import os
import sys
import subprocess

STANFORD_CORENLP_3_4_1_JAR = 'stanford-corenlp-3.4.1.jar'
#print STANFORD_CORENLP_3_4_1_JAR

PUNCTUATIONS = ["''", "'", "``", "`", "-LRB-", "-RRB-", "-LCB-", "-RCB-", \
        ".", "?", "!", ",", ":", "-", "--", "...", ";"] 

class PTBTokenizer:
    """Python wrapper of Stanford PTBTokenizer"""

    def tokenize(self, captions_for_image):
        cmd = ['java', '-cp', STANFORD_CORENLP_3_4_1_JAR, \
                'edu.stanford.nlp.process.PTBTokenizer', \
                '-preserveLines', '-lowerCase']

        tokenized_captions_for_image = dict()
        images = []
        sentences = ''
        for k, v in captions_for_image.iteritems():
            tokenized_captions_for_image[k] = []
            idx_c = 0
            assert(type(v) is list)
            for c in v:
                tokenized_captions_for_image[k].append([])
                idx_s = 0
                for s in c.split('\n'):
                    images.append((k, idx_c, idx_s))
                    idx_s += 1
                    tokenized_captions_for_image[k][-1].append(None)
                    sentences += s
                    sentences += '\n'
                idx_c += 1

        # Note: need to be called in current directory (using cwd argument)
        p_tokenizer = subprocess.Popen(cmd, \
                cwd=os.path.dirname(os.path.abspath(__file__)), \
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, \
                stderr=subprocess.PIPE)
        token_lines = p_tokenizer.communicate(input=sentences.rstrip())[0]
        idx = 0
        for line in token_lines.split('\n'):
            k, idx_c, idx_s = images[idx]
            tokenized_caption = ' '.join([w for w in line.rstrip().split(' ') \
                    if w not in PUNCTUATIONS])
            tokenized_captions_for_image[k][idx_c][idx_s] = tokenized_caption
            idx += 1

        final_tokenized_captions_for_image = dict()
        for k, v in tokenized_captions_for_image.iteritems():
            final_tokenized_captions_for_image[k] = []
            for c in v:
                final_tokenized_captions_for_image[k].append('\n'.join(c))

        return final_tokenized_captions_for_image
