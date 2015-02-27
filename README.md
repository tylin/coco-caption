Microsoft COCO Caption Evaluation
===================

Evaluation codes for MS COCO caption generation.

## REQUIREMENTS ##
- java 1.8.0
- python 2.7

## FILES ##
./
- evaluate_caption.py: demo script

./data
- captions_val2014.json
		The caption annotations of COCO2014 validation set.
		It can be downloaded from http://mscoco.org/download
- captions_val2014_submission.json:
        The generated captions for evaluation.
        The format is:
		[{"image_id": int, "caption": str}]

./caption_eval: This is a folder where all evaluation codes are stored.
- evals.py: includes Python classes of different methods.
- utils.py: utility functions for parsing data.
- tokenizer: PTBTokenizer
- bleu: Bleu evalutation codes
- meteor: Meteor evaluation codes
- rouge: Rouge evaluation codes
- cider: CIDEr evaluation codes