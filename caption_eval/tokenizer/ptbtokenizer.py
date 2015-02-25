#!/usr/bin/env python
# 
# File Name : ptbtokenizer.py
#
# Description : Do the PTB Tokenization and remove punctuations.
#
# Usage :
#
# Creation Date : 29-12-2014
# Last Modified : Wed 25 Feb 2015 01:41:30 PM PST
# Author : Hao Fang

import os
import sys
import subprocess
import tempfile

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

        print >> sys.stderr, "preparing the input for Stanford PTBTokenizer..."
        tokenized_captions_for_image = dict()
        images = []
        list_sentences = []
        for k, v in captions_for_image.iteritems():
            tokenized_captions = []
            idx_c = 0
            assert(type(v) is list)
            for c in v:
                tokenized_captions.append([])
                idx_s = 0
                for s in c.splitlines():
                    images.append((k, idx_c, idx_s))
                    idx_s += 1
                    tokenized_captions[-1].append(None)
                    list_sentences.append(s)
                idx_c += 1
            tokenized_captions_for_image[k] = tokenized_captions
        list_sentences.append('')
        sentences = '\n'.join(list_sentences)

        print >> sys.stderr, "tokenizing..."
        # Note: need to be called in current directory (using cwd argument)
        path_to_jar_dirname=os.path.dirname(os.path.abspath(__file__))
        tmp_file = tempfile.NamedTemporaryFile(delete=False, dir=path_to_jar_dirname)
        tmp_file.write(sentences)
        tmp_file.close()
        cmd.append(os.path.basename(tmp_file.name))
        p_tokenizer = subprocess.Popen(cmd, cwd=path_to_jar_dirname, \
                stdout=subprocess.PIPE)
        #p_tokenizer = subprocess.Popen(cmd, \
        #        cwd=os.path.dirname(os.path.abspath(__file__)), \
        #        stdin=subprocess.PIPE, stdout=subprocess.PIPE, \
        #        stderr=subprocess.PIPE)
        #token_lines = p_tokenizer.communicate(input=sentences.rstrip())[0]
        token_lines = p_tokenizer.communicate()[0]
        os.remove(tmp_file.name)

        print >> sys.stderr, "processing the output of Stanford PTBTokenizer..."
        idx = 0
        for line in token_lines.splitlines():
            k, idx_c, idx_s = images[idx]
            tokenized_caption = ' '.join([w for w in line.rstrip().split(' ') \
                    if w not in PUNCTUATIONS])
            tokenized_captions_for_image[k][idx_c][idx_s] = tokenized_caption
            idx += 1

        print >> sys.stderr, "prepare the json data..."
        final_tokenized_captions_for_image = dict()
        for k, v in tokenized_captions_for_image.iteritems():
            final_tokenized_captions_for_image[k] = []
            for c in v:
                final_tokenized_captions_for_image[k].append('\n'.join(c))

        return final_tokenized_captions_for_image
