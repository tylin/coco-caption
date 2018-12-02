'''
Special thanks to Mert Kilickaya, first author of 'Re-evaluating Automatic Metrics for Image Captioning' [http://aclweb.org/anthology/E17-1019] for giving exact instructions on how to implement the Word Mover's Distance metric here.
'''

import numpy as np
import gensim
import os

class WMD:

    def __init__(self):
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'stopwords.txt'), 'r', encoding='utf-8') as f:
            self.stop_words = set(f.read().strip().split(' ')) #Stop words were taken from NLTK nltk.stopwords.words('english')
        self.model = gensim.models.KeyedVectors.load_word2vec_format(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'GoogleNews-vectors-negative300.bin'), binary=True)
        self.sigma = 1.0
        
    def calc_score(self, candidate, refs):
        scores = list()
        c_tokens = [ token for token in candidate[0].split(' ') if token not in self.stop_words ]
        for ref in refs:
            r_tokens = [ token for token in ref.split(' ') if token not in self.stop_words ]
            dist = self.model.wmdistance(c_tokens, r_tokens)
            score = np.exp(-dist/self.sigma)
            scores.append(score)
        return max(scores)
    
    def compute_score(self, gts, res):
        assert(sorted(gts.keys()) == sorted(res.keys()))
        imgIds = sorted(gts.keys())

        score = []
        for id in imgIds:
            hypo = res[id]
            ref  = gts[id]

            score.append(self.calc_score(hypo, ref))

            # Sanity check.
            assert(type(hypo) is list)
            assert(len(hypo) == 1)
            assert(type(ref) is list)
            assert(len(ref) >= 1)

        average_score = np.mean(np.array(score))
        return average_score, np.array(score)
    
    def method(self):
        return "WMD"
