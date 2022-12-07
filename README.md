Microsoft COCO Caption Evaluation
===================

Evaluation codes for MS COCO caption generation.

## Description ##
This repository provides Python 3 support for the caption evaluation metrics used for the MS COCO dataset.

The code is derived from the original repository that supports Python 2.7: https://github.com/tylin/coco-caption.  
Caption evaluation depends on the COCO API that natively supports Python 3.

## Requirements ##
- Java 1.8.0
- Python 3

## Installation ##
To install pycocoevalcap and the pycocotools dependency (https://github.com/cocodataset/cocoapi), run:
```
pip install pycocoevalcap
```

## Usage ##
See the example script: [example/coco_eval_example.py](example/coco_eval_example.py)

## Files ##
./
- eval.py: The file includes COCOEavlCap class that can be used to evaluate results on COCO.
- tokenizer: Python wrapper of Stanford CoreNLP PTBTokenizer
- bleu: Bleu evalutation codes
- meteor: Meteor evaluation codes
- rouge: Rouge-L evaluation codes
- cider: CIDEr evaluation codes
- spice: SPICE evaluation codes

## Setup ##

- SPICE requires the download of [Stanford CoreNLP 3.6.0](http://stanfordnlp.github.io/CoreNLP/index.html) code and models. This will be done automatically the first time the SPICE evaluation is performed.
- Note: SPICE will try to create a cache of parsed sentences in ./spice/cache/. This dramatically speeds up repeated evaluations. The cache directory can be moved by setting 'CACHE_DIR' in ./spice. In the same file, caching can be turned off by removing the '-cache' argument to 'spice_cmd'.

## References ##

- [Microsoft COCO Captions: Data Collection and Evaluation Server](http://arxiv.org/abs/1504.00325)
- PTBTokenizer: We use the [Stanford Tokenizer](http://nlp.stanford.edu/software/tokenizer.shtml) which is included in [Stanford CoreNLP 3.4.1](http://nlp.stanford.edu/software/corenlp.shtml).
- BLEU: [BLEU: a Method for Automatic Evaluation of Machine Translation](http://www.aclweb.org/anthology/P02-1040.pdf)
- Meteor: [Project page](http://www.cs.cmu.edu/~alavie/METEOR/) with related publications. We use the latest version (1.5) of the [Code](https://github.com/mjdenkowski/meteor). Changes have been made to the source code to properly aggreate the statistics for the entire corpus.
- Rouge-L: [ROUGE: A Package for Automatic Evaluation of Summaries](http://anthology.aclweb.org/W/W04/W04-1013.pdf)
- CIDEr: [CIDEr: Consensus-based Image Description Evaluation](http://arxiv.org/pdf/1411.5726.pdf)
- SPICE: [SPICE: Semantic Propositional Image Caption Evaluation](https://arxiv.org/abs/1607.08822)

## Developers ##
- Xinlei Chen (CMU)
- Hao Fang (University of Washington)
- Tsung-Yi Lin (Cornell)
- Ramakrishna Vedantam (Virgina Tech)

## Acknowledgement ##
- David Chiang (University of Norte Dame)
- Michael Denkowski (CMU)
- Alexander Rush (Harvard University)
