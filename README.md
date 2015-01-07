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
- id.txt: 
- hypo.txt: uploaded hypothese (un-tokenized)
- tokenized_ref.txt: tokenized references
hypo.txt and tokenized_ref.txt should be aligned according to id.txt.
Each line of hypo.txt is a hpyo for the corresponding line in id.txt.
Every 5 lines of tokenized_ref.txt are the references for a line in id.txt.

./caption_eval: This is a folder where all evaluation codes are stored.
- evals.py: includes Python classes of different methods.
- tokenizer: PTBTokenizer
- bleu: Bleu evalutation codes
- meteor: Meteor evaluation codes
- rouge: Rouge evaluation codes
- cidr: Cidr evaluation codes
