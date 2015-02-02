#!/usr/bin/env python

import os
import sys
import subprocess
import threading

# Assumes meteor-1.5.jar is in the same directory as meteor.py.  Change as needed.
METEOR_JAR = 'meteor-1.5.jar'
# print METEOR_JAR

class Meteor:

    def __init__(self):
        self.meteor_cmd = ['java', '-jar', '-Xmx2G', METEOR_JAR, \
                '-', '-', '-stdio', '-l', 'en', '-norm']
        self.meteor_p = subprocess.Popen(self.meteor_cmd, \
                cwd=os.path.dirname(os.path.abspath(__file__)), \
                stdin=subprocess.PIPE, \
                stdout=subprocess.PIPE, \
                stderr=subprocess.PIPE)
        # Used to guarantee thread safety
        self.lock = threading.Lock()

    def compute_score(self, hypo_for_image, ref_for_image):
        images = hypo_for_image.keys()
        images.sort()
        tmp_images = ref_for_image.keys()
        tmp_images.sort()
        assert(images == tmp_images)

        scores = []
        for i in images:
            assert(len(hypo_for_image[i]) == 1)
            # TODO: get score? not sure if it is correct.
            scores.append(self._score(hypo_for_image[i][0], ref_for_image[i]))

        return sum(scores)/len(scores)


    def method(self):
        return "METEOR"

    def _score(self, hypothesis_str, reference_list):
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
