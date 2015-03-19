Microsoft COCO Caption Evaluation
===================

Evaluation codes for MS COCO caption generation.

## Requirements ##
- java 1.8.0
- python 2.7

## Files ##
./
- cocoEvalCapDemo.py (demo script)

./annotation
- captions_val2014.json (COCO 2014 caption validation set)
- More detials can be found under download tab on [COCO dataset](http://mscoco.org/dataset)

./results
- captions_val2014_fakecap_results.json (example fake results for running demo)
- More details can be found under evaluate->format tab on [COCO dataset](http://mscoco.org/dataset)

./pycocoevalcap: The folder where all evaluation codes are stored.
- evals.py: The file includes COCOEavlCap class that can be used to evaluate results on COCO.
- tokenizer: Python wrapper of Stanford CoreNLP PTBTokenizer
- bleu: Bleu evalutation codes
- meteor: Meteor evaluation codes
- rouge: Rouge-L evaluation codes
- cider: CIDEr evaluation codes

## References ##

- PTBTokenizer: We use the [Stanford Tokenizer](http://nlp.stanford.edu/software/tokenizer.shtml) which is included in [Stanford CoreNLP 3.4.1](http://nlp.stanford.edu/software/corenlp.shtml).
- BLEU: [BLEU: a Method for Automatic Evaluation of Machine Translation](http://delivery.acm.org/10.1145/1080000/1073135/p311-papineni.pdf?ip=72.229.132.206&id=1073135&acc=OPEN&key=4D4702B0C3E38B35%2E4D4702B0C3E38B35%2E4D4702B0C3E38B35%2E6D218144511F3437&CFID=644819513&CFTOKEN=71377947&__acm__=1426607117_16e4342fbc20d41c064c8fb685cffe60)
- Meteor: [Project page](http://www.cs.cmu.edu/~alavie/METEOR/) with related publications. We use the latest version (1.5) of the [Code](https://github.com/mjdenkowski/meteor). Changes have been made to the source code to properly aggreate the statistics for the entire corpus.
- Rouge-L: [ROUGE: A Package for Automatic Evaluation of Summaries](http://anthology.aclweb.org/W/W04/W04-1013.pdf)
- CIDEr: [CIDEr: Consensus-based Image Description Evaluation] (http://arxiv.org/pdf/1411.5726.pdf)

## Developers ##
- Xinlei Chen (CMU)
- Hao Fang (University of Washington)
- Tsung-Yi Lin (Cornell)
- Ramakrishna Vedantam (Virgina Tech)

## Acknowledgement ##
- David Chiang (University of Norte Dame)
- Michael Denkowski (CMU)
- Alexander Rush (Harvard University)
