#!/usr/bin/env python
# 
# File Name : bleu.py
#
# Description :
#
# Usage :
#
# Creation Date : 06-01-2015
# Last Modified : Tue Jan  6 16:52:46 2015
# Author : Hao Fang

from bleu_scorer import BleuScorer


class Bleu:
    def compute_score(self, hypo_txt_file, ref_txt_file, num_refs_per_hypo):
        hypo_lines = []
        for line in hypo_txt_file:
            hypo_lines.append(line.rstrip())
        
        ref_lines = []
        for i, line in enumerate(ref_txt_file):
            if i % num_refs_per_hypo == 0:
                ref_lines.append([])
            ref_lines[-1].append(line.rstrip())

        bleu_scorer = BleuScorer()

        for (h, r) in zip(hypo_lines, ref_lines):
            bleu_scorer += (h, r)

        bleu, bleu_info = bleu_scorer.compute_score(option='shortest')

        return (bleu, bleu_info)

    def method(self):
        return "Bleu"
