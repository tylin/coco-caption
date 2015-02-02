#!/usr/bin/env python

# =================================================
# Specify file path
# =================================================
path_to_tokenized_ref_json = 'data/tokenized_ref.json'
path_to_raw_hypo_json = 'data/hypo.json'

# from caption_eval.evals import PTBTokenizer, Bleu, Rouge, Meteor, Cider
from caption_eval.evals import PTBTokenizer, Bleu, Rouge, Meteor

# =================================================
# Load references
# Two reference Test5 and Test40
# =================================================
import json
tokenized_ref_for_image_test5 = json.load(open(path_to_tokenized_ref_json))
# still collecting test40.  will replace this when crowd-sourcing is done
tokenized_ref_for_image_test40 = json.load(open(path_to_tokenized_ref_json))
tokenized_ref_for_image_test = [(tokenized_ref_for_image_test5, 'test5'), (tokenized_ref_for_image_test40, 'test40')]

# =================================================
# Tokenize hypotheses
# =================================================
print 'tokenizing hypothese...'
raw_hypo_for_image = json.load(open(path_to_raw_hypo_json))
tokenizer = PTBTokenizer()
tokenized_hypo_for_image= tokenizer.tokenize(raw_hypo_for_image)
hypo_keys = tokenized_hypo_for_image.keys()
test5_keys = tokenized_ref_for_image_test5.keys()
assert(set(test5_keys)  == set(hypo_keys) )
print 'all hypothese have been tokenized'

# =================================================
# Set up scorers
# =================================================
scorers = [
    (Bleu(1), "B1"),
    (Bleu(2), "B2"),
    (Bleu(3), "B3"),
    (Bleu(4), "B4"),
    (Meteor(),"METEOR"),
    (Rouge(), "ROUGE"),
    # (Cider(), "CIDER")
]

# =================================================
# Compute scores
# =================================================
scores = {}
for scorer, alg in scorers:
    for tokenized_ref_for_image, testset in tokenized_ref_for_image_test:
        score = scorer.compute_score(tokenized_hypo_for_image, \
            tokenized_ref_for_image)
        print alg, testset, score
        # for CodaLab to easily generate scoring table
        scores[alg+testset] = score

print scores