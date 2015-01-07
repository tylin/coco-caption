#!/usr/bin/env python
# 
# File Name : bleu.py
#
# Description :
#
# Usage :
#
# Creation Date : 06-01-2015
# Last Modified : Tue Jan  6 22:34:41 2015
# Author : Hao Fang

from bleu_scorer import BleuScorer


class Bleu:
    def compute_score(self, hypo_for_image, ref_for_image):
        images = hypo_for_image.keys()
        images.sort()
        tmp_images = ref_for_image.keys()
        tmp_images.sort()
        assert(images == tmp_images)

        bleu_scorer = BleuScorer()
        for i in images:
            hypo = hypo_for_image[i]
            ref = ref_for_image[i]

            # Sanity check.
            assert(type(hypo) is list)
            assert(len(hypo) == 1)
            assert(type(ref) is list)
            assert(len(ref) > 0)

            bleu_scorer += (hypo[0], ref)

        bleu, bleu_info = bleu_scorer.compute_score(option='shortest')

        return (bleu, bleu_info)

    def method(self):
        return "Bleu"
