# Filename: cider.py
#
# Description: Describes the class to compute the CIDEr Metric
#
# Creation Date: Sun Feb  8 14:16:54 2015
#
# Author: Tsung-Yi Lin

from cider_scorer import CiderScorer

class Cider:
    """
    Main Class to compute the CIDEr metric described at : http://arxiv.org/abs/1411.5726

    """
    def __init__(self, test=None, refs=None, n=4):
        # set cider to sum over 1 to 4-grams
        self._n = 4

    def compute_score(self, hypo_for_image, ref_for_image):
        images = hypo_for_image.keys()
        images.sort()
        tmp_images = ref_for_image.keys()
        tmp_images.sort()
        assert(images == tmp_images)

        cider_scorer = CiderScorer(n=self._n)
        for i in images:
            hypo = hypo_for_image[i]
            ref = ref_for_image[i]

            # Sanity check.
            assert(type(hypo) is list)
            assert(len(hypo) == 1)
            assert(type(ref) is list)
            assert(len(ref) > 0)

            cider_scorer += (hypo[0], ref)

        cider = cider_scorer.compute_score()

        # return (bleu, bleu_info)
        return cider

    def method(self):
        return "CIDEr"