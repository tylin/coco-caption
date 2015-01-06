#!/usr/bin/env python
# 
# File Name : ptbtokenizer.py
#
# Description :
#
# Usage :
#
# Creation Date : 29-12-2014
# Last Modified : Tue 06 Jan 2015 01:19:12 PM PST
# Author : Hao Fang

import os
import sys
import subprocess

STANFORD_CORENLP_3_4_1_JAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), \
        'stanford-corenlp-3.4.1.jar')
# print STANFORD_CORENLP_3_4_1_JAR

class PTBTokenizer:
    """Python wrapper of Stanford PTBTokenizer"""

    def __init__(self):
        self._tokenizer_cmd = ['java', '-cp', STANFORD_CORENLP_3_4_1_JAR, \
                'edu.stanford.nlp.process.PTBTokenizer', \
                '-preserveLines', '-lowerCase']

    def tokenize(self, str):
        p_echo = subprocess.Popen(['echo', str], \
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p_tokenizer = subprocess.Popen(self._tokenizer_cmd, \
                stdin=p_echo.stdout, stdout=subprocess.PIPE, \
                stderr=subprocess.PIPE)
        p_echo.stdout.close()
        # not include the '\n' at the end 
        # do not use rstrip in case '\n' is in the str
        tokens = p_tokenizer.communicate()[0][:-1]
        return tokens
