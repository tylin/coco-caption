#!/usr/bin/env python

import os
import sys
import subprocess
import threading

# Assumes meteor-1.5.jar is in the same directory as meteor.py.  Change as needed.
METEOR_JAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meteor-1.5.jar')
print METEOR_JAR
class Meteor:

    def __init__(self):
        self.meteor_cmd = ['java', '-jar', '-Xmx2G', METEOR_JAR, '-', '-', '-stdio']
        self.meteor_p = subprocess.Popen(self.meteor_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # Used to guarantee thread safety
        self.lock = threading.Lock()
        print "TODO: testing meteor"

    def compute_score(self, test, ref):
        print "COMPUTE_SCORE HASN'T BEEN DEFINED"
        return -1.00

    def method(self):
        return "METEOR"

    def score(self, hypothesis_str, reference_list):
        self.lock.acquire()
        # SCORE ||| reference 1 words ||| reference n words ||| hypothesis words
        score_line = ' ||| '.join(('SCORE', ' ||| '.join(reference_list), hypothesis_str))
        self.meteor_p.stdin.write('{}\n'.format(score_line))
        stats = self.meteor_p.stdout.readline().strip()
        eval_line = 'EVAL ||| {}'.format(stats)
        # EVAL ||| stats
        self.meteor_p.stdin.write('{}\n'.format(eval_line))
        score = float(self.meteor_p.stdout.readline().strip())
        self.lock.release()
        return score
 
    def close(self):
        self.lock.acquire()
        self.meteor_p.stdin.close()
        self.meteor_p.wait()
        self.lock.release()

# # Test the above class
# meteor = Meteor()
# # 1.0
# print meteor.score('this scores perfectly .', ['this scores perfectly .'])
# # 1.0
# print meteor.score('this also scores perfectly .', ['this scores badly .', 'this also scores perfectly .'])
# # 0.0484848484848
# print meteor.score('this scores badly .', ['this isn \'t the text you \'re looking for .'])
# meteor.close()
