__author__ = 'tylin'

from caption_eval.evals import Bleu, Rouge, Meteor, Cider
import caption_eval.preprocess as preprocess

# =================================================
# Load Data from JSON file
# The data is pairs of key(image_id) and value(caption(s))
# refs is reference captions
#
# =================================================
import json
print 'loading test captions...'
tests_raw = json.load(open('misc/sentence_test.json'))
print 'loading reference captions...'
refs_raw = json.load(open('misc/sentence_ref.json'))



# =================================================
# Preprocessing Data
# INPUT: list of captions
#        for testing captions, it is an array of object with key (image id) and value (single caption).
#        for testing captions, it is an array of object with key (image id) and value (list of captions).
# OUTPUT: normalized captions in python object with key (image id) and value (list of words)
# =================================================
print 'normalizing test captions, process %d captions...'%(len(tests_raw))
tests = preprocess.normalize_captions(tests_raw)
print 'normalizing refs captions, process %d captions...'%(sum(map(lambda x: len(x[1][0]), refs_raw.items())))
refs = preprocess.normalize_captions(refs_raw)
print 'all captions have been tokenized as a list of words'

# =================================================
# Evaluation
# INPUT: pair of preprocessed tests and refs data
# OUTPUT: single value score
# All the evaluation methods are defined in class
# The class shares three member functions
#   score = eval.compute_score(tests, refs)
#       compute score given the test and ref data
#   method = eval.method()
#       show name of eval method
# =================================================
evals = [Bleu(),
         Meteor(),
         Rouge(),
         Cider()]
for eval in evals:
    s = eval.compute_score(tests, refs)
    print "%s score: %0.2f"%(eval.method(), s)