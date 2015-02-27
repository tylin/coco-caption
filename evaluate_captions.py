__version__ = 1.0
# Evaluation software for evaluating image captioning task

# Microsoft COCO is a large image dataset designed for object detection,
# segmentation, and caption generation. caption_eval is a Python module that
# evaluates caption generation for COCO images.
# Please visit http://mscoco.org/ for more information on COCO, including
# for the data, paper, and tutorials. The exact format of the annotations
# is also described on the COCO website.

# This software can be used to evaluate image captioning performance on COCO validation set locally.
# The COCO image captioning evaluation server will use the same code for evaluation.
# Following shows the data format for submitting to the evaluation server.

# File name: captions_[split]_submission.json, e.g., captions_val2014_submission.json
# The submission file format is an array of object:
# [{
#   "image_id": int,
#   "caption": str,
# }]
#
#
# Microsoft COCO caption evaluation Toolbox.      Version 1.0
# Data, paper, and tutorials available at:  http://mscoco.org/
# Code written by:  Xinlei Chen          (CMU)
#                   Hao Feng             (Univ. of Washington)
#                   Tsung-Yi Lin         (Cornell)
#                   Ramakrishna Vedantam (Virginia Tech)
# Licensed under the Simplified BSD License [see bsd.txt]

from caption_eval.evals import PTBTokenizer, Bleu, Rouge, Meteor, Cider
from caption_eval.util import pack_coco_annotations, pack_coco_submission

# =================================================
# specify the path to reference caption file and
# submission caption file
# In this demo hypo is randomly selected from
# the original validation set
# =================================================
path_to_raw_ref_json  = 'data/captions_val2014.json'
path_to_raw_hypo_json = 'data/captions_val2014_submission.json'

# =================================================
# loading JSON reference and hypo file
# =================================================
print 'loading hypo and ref JSON file...'
raw_ref_for_image  = pack_coco_annotations(path_to_raw_ref_json)
raw_hypo_for_image = pack_coco_submission(path_to_raw_hypo_json)

# ================================================
# check hypothese captions include all images
# in reference captions
# ================================================
ref_keys  = raw_ref_for_image.keys().sort()
hypo_keys = raw_hypo_for_image.keys().sort()
assert(ref_keys==hypo_keys)

# =================================================
# Load references
# The reference is 4 captions from COCO val2014
# =================================================
print 'tokenization...'
tokenizer = PTBTokenizer()
tokenized_ref_for_image  = tokenizer.tokenize(raw_ref_for_image)
tokenized_hypo_for_image = tokenizer.tokenize(raw_hypo_for_image)

# =================================================
# Set up scorers
# =================================================
print 'setting up scorers...'
scorers = [
    (Bleu(4), ["B1", "B2", "B3", "B4"]),
    (Meteor(),"METEOR"),
    (Rouge(), "ROUGE"),
    (Cider(), "CIDER")
]

# =================================================
# Compute scores
# =================================================
scores = {}
for scorer, method in scorers:
    print 'computing %s score...'%(scorer.method())
    score = scorer.compute_score(tokenized_hypo_for_image, tokenized_ref_for_image)
    if type(score) == list:
        for s, m in zip(score, method):
            scores[m] = s
            print m, s
    else:
        scores[method] = score
        print method, score

print scores