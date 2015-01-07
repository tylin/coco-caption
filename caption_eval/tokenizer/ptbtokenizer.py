#!/usr/bin/env python
# 
# File Name : ptbtokenizer.py
#
# Description :
#
# Usage :
#
# Creation Date : 29-12-2014
# Last Modified : Tue Jan  6 16:46:07 2015
# Author : Hao Fang

import os
import sys
import subprocess

STANFORD_CORENLP_3_4_1_JAR = 'stanford-corenlp-3.4.1.jar'
#print STANFORD_CORENLP_3_4_1_JAR

class PTBTokenizer:
    """Python wrapper of Stanford PTBTokenizer"""

    def tokenize(self, infile):
        cmd = ['java', '-cp', STANFORD_CORENLP_3_4_1_JAR, \
                'edu.stanford.nlp.process.PTBTokenizer', \
                '-preserveLines', '-lowerCase']
        # Note: need to be called in current directory (using cwd argument)
        p_tokenizer = subprocess.Popen(cmd, \
                cwd=os.path.dirname(os.path.abspath(__file__)), \
                stdin=infile, stdout=subprocess.PIPE, \
                stderr=subprocess.PIPE)
        token_lines = []
        for line in p_tokenizer.stdout:
            token_lines.append(line.rstrip())
        p_tokenizer.stdout.close()
        return token_lines
