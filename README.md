mscoco_caption_eval
===================

Evaluation codes for mscoco caption generation.

## REQUIREMENTS ##
- java 1.8.0
- python 2.7

## FILES ##
./
- evaluate_caption.py: demo script

./data
- hypo.json: uploaded hypothese (un-tokenized)
- tokenized_ref.json: tokenized references

./caption_eval: This is a folder where all evaluation codes are stored.
- evals.py: includes Python classes of different methods.
- tokenizer: PTBTokenizer
- bleu: Bleu evalutation codes
- meteor: Meteor evaluation codes
- rouge: Rouge evaluation codes
- cidr: Cidr evaluation codes

./misc: Miscellaneous files and scripts.
