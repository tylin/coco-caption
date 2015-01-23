from nltk.tokenize import wordpunct_tokenize

def tokenize(X, context=5, start='<start>', end='<end>'):
    """
    Tokenize each of the captions
    """
    tokens = [wordpunct_tokenize(x) for x in X]
    tokens = [ [w.lower() for w in x] for x in tokens ]
    tokens = [ [is_number(w) for w in x] for x in tokens ]
    for i, x in enumerate(tokens):
        tokens[i] = [start] * context + x + [end]
    return tokens

class Cider:
    '''
    TODO: define Rouge class
    '''
    def __init__(self):
        print 'TODO: define CIDEr class'

    def compute_score(self, test, ref):

        print "inside compute_score"
        tokens =  tokenize(ref)
        print tokens
        return 1

    def method(self):
        return "CIDEr"