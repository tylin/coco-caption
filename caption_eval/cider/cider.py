from utils import lm_tools
import pdb

def split_dataset(dataset):
    tokens = {}
    for image in dataset:
        sents = dataset[image]
        sp_sents = ();
        for sent in sents:
            assert(type("a") == type(sent))
            sp_sents.append(sent.split())
        tokens[image] = sp_sents

    return tokens

def is_number(s):
    try:
        float(s)
        return '<#>'
    except ValueError:
        return s

class Cider:
    '''
    TODO: define Rouge class
    '''
    def __init__(self):
        print 'TODO: define CIDEr class'

    def compute_score(self, test, ref):

        print "inside compute_score"
        test_split = split_dataset(test)
        pdb.set_trace()
        print tokens
        return 1

    def method(self):
        return "CIDEr"