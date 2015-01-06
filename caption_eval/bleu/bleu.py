#!/usr/bin/env python
# 
# File Name : bleu.py
#
# Description :
#
# Usage :
#
# Creation Date : 06-01-2015
# Last Modified : Tue Jan  6 13:02:11 2015
# Author : Hao Fang

from bleu_scorer import BleuScorer


class Bleu:
    def compute_score(self, hypos_json, refs_json):
        hypos = []
        refs = []

        bleu_scorer = BleuScorer()
        for i, r in refs_json.iteritems():
            print i, r, hypos_json[i]
            bleu_scorer += (hypos_json[i], r)

        bleu = bleu_scorer.compute_score(option='shortest')
        return bleu

    def method(self):
        return "Bleu"
