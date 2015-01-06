#!/usr/bin/env python

# bleu.py
# David Chiang <chiang@isi.edu>

# Copyright (c) 2004-2006 University of Maryland. All rights
# reserved. Do not redistribute without permission from the
# author. Not for commercial use.

'''Provides:
cook_refs(refs, n=4): Transform a list of reference sentences as strings into a form usable by cook_test().
cook_test(test, refs, n=4): Transform a test sentence as a string (together with the cooked reference sentences) into a form usable by score_cooked().
score_cooked(alltest, n=4): Score a list of cooked test sentences.
The reason for breaking the BLEU computation into three phases cook_refs(), cook_test(), and score_cooked() is to allow the caller to calculate BLEU scores for multiple test sets as efficiently as possible.
'''

import optparse
import copy
import sys, math, re, xml.sax.saxutils
from collections import defaultdict

import gflags as flags
FLAGS=flags.FLAGS

flags.DEFINE_boolean("preserve_case", True, "preserve case", short_name="c")
flags.DEFINE_boolean("nist_tokenize", True, "nist tokenize")
flags.DEFINE_boolean("clip_len", False, "clip length")
flags.DEFINE_string("eff_ref_len", "closest", "effective length ratio: closest, average, shortest", short_name="len")    
flags.DEFINE_boolean("latin", False, "remove non-latin_1 chars")
flags.DEFINE_boolean("debug_cook", False, "output cooked test")

logs = sys.stderr

normalize1 = [
    ('<skipped>', ''),         # strip "skipped" tags
    (r'-\n', ''),              # strip end-of-line hyphenation and join lines
    (r'\n', ' '),              # join lines
#    (r'(\d)\s+(?=\d)', r'\1'), # join digits
]
normalize1 = [(re.compile(pattern), replace) for (pattern, replace) in normalize1]

# { | } ~      [ \ ] ^ _ `   (sp) ! " # $ % &    ( ) * +    : ; < = > ? @  /
normalize2 = [
    (r'([\{-\~\[-\` -\&\(-\+\:-\@\/])',r' \1 '), # tokenize punctuation. apostrophe is missing
    (r'([^0-9])([\.,])',r'\1 \2 '),              # tokenize period and comma unless preceded by a digit
    (r'([\.,])([^0-9])',r' \1 \2'),              # tokenize period and comma unless followed by a digit
    (r'([0-9])(-)',r'\1 \2 ')                    # tokenize dash when preceded by a digit
]
normalize2 = [(re.compile(pattern), replace) for (pattern, replace) in normalize2]

def normalize(s):
    '''Normalize and tokenize text. This is lifted from NIST mteval-v11a.pl.'''
    if type(s) is not str:
        s = " ".join(s)
    # language-independent part:
    for (pattern, replace) in normalize1:
        s = re.sub(pattern, replace, s)
    s = xml.sax.saxutils.unescape(s, {'&quot;':'"'}) # &amp; &lt; &gt; ?
    # language-dependent part (assuming Western languages):
    s = " %s " % s
    if not FLAGS.preserve_case:
        s = s.lower()         # this might not be identical to the original
    for (pattern, replace) in normalize2:
        s = re.sub(pattern, replace, s)
    return s.split()

def precook(s, n=4, out=False):
    """Takes a string as input and returns an object that can be given to
    either cook_refs or cook_test. This is optional: cook_refs and cook_test
    can take string arguments as well."""
    if type(s) is str or type(s) is unicode:
        if FLAGS.nist_tokenize:
            words = normalize(s)
        else:
            words = s.split()
        counts = defaultdict(int)
        for k in xrange(1,n+1):
            for i in xrange(len(words)-k+1):
                ngram = tuple(words[i:i+k])
                counts[ngram] += 1
        return (len(words), counts)
    else:
        return s

def cook_refs(refs, eff=None, n=4): ## lhuang: oracle will call with "average"
    '''Takes a list of reference sentences for a single segment
    and returns an object that encapsulates everything that BLEU
    needs to know about them.'''

    reflen = []
    maxcounts = {}
    for ref in refs:
        rl, counts = precook(ref, n)
        reflen.append(rl)
        for (ngram,count) in counts.iteritems():
            maxcounts[ngram] = max(maxcounts.get(ngram,0), count)

    # Calculate effective reference sentence length.
    if eff == "shortest":
        reflen = min(reflen)
    elif eff == "average":
        reflen = float(sum(reflen))/len(reflen)

    ## lhuang: N.B.: leave reflen computaiton to the very end!!
    
    ## lhuang: N.B.: in case of "closest", keep a list of reflens!! (bad design)

    return (reflen, maxcounts)

def cook_test(test, (reflen, refmaxcounts), eff=None, n=4):
    '''Takes a test sentence and returns an object that
    encapsulates everything that BLEU needs to know about it.'''

    testlen, counts = precook(test, n, True)

    result = {}

    # Calculate effective reference sentence length.
    
    if eff == "closest":
        result["reflen"] = min((abs(l-testlen), l) for l in reflen)[1]
    else: ## i.e., "average" or "shortest" or None
        result["reflen"] = reflen

##    result["reflen"] = reflen ## keep all, and let scorer decide eff_len

    if FLAGS.clip_len:
        result["testlen"] = min(testlen, result["reflen"])
    else:
        result["testlen"] = testlen

    result["guess"] = [max(0,testlen-k+1) for k in xrange(1,n+1)]

    result['correct'] = [0]*n
    for (ngram, count) in counts.iteritems():
        result["correct"][len(ngram)-1] += min(refmaxcounts.get(ngram,0), count)

    return result

def score_cooked(allcomps, n=4, addprec=0):
    totalcomps = {'testlen':0, 'reflen':0, 'guess':[0]*n, 'correct':[0]*n}
    for comps in allcomps:
        for key in ['testlen','reflen']:
            totalcomps[key] += comps[key]
        for key in ['guess','correct']:
            for k in xrange(n):
                totalcomps[key][k] += comps[key][k]
    bleu = 1.
    for k in xrange(n):
        bleu *= float(totalcomps['correct'][k]+addprec)/(totalcomps['guess'][k]+addprec)
    bleu = bleu ** (1./n)
    len_ratio = totalcomps['testlen']/float(totalcomps['reflen'])
    if len_ratio < 1: #0 < totalcomps['testlen'] < totalcomps['reflen']:        
        bleu *= math.exp(len_ratio-1)

    if verbose:
        sys.stderr.write("hyp words: %s\n" % totalcomps['testlen'])
        sys.stderr.write("effective reference length: %s\n" % totalcomps['reflen'])
        

    if verbose:
        for k in xrange(n):
            prec = float(totalcomps['correct'][k]+addprec)/(totalcomps['guess'][k]+addprec)
            sys.stderr.write("%d-gram precision:  %s\n" % (k+1,prec))
    if verbose:
        sys.stderr.write("length ratio:      %s\n" % (float(totalcomps['testlen'])/totalcomps['reflen']))
        
    return bleu, len_ratio

class Bleu(object):

    __slots__ = "n", "crefs", "ctest", "_score", "_ratio", "_testlen", "_reflen", "special_reflen"
    # special_reflen is used in oracle (proportional effective ref len for a node).

    def copy(self):
        ''' copy the refs.'''
        new = Bleu(n=self.n)
        new.ctest = copy.copy(self.ctest)
        new.crefs = copy.copy(self.crefs)
        new._score = None
        return new

    def __init__(self, test=None, refs=None, n=4, special_reflen=None):
        ''' singular instance '''
        self.n = n
        self.crefs = []
        self.ctest = []
        self.cook_append(test, refs)
        self.special_reflen = special_reflen

    def compute_score(self, test, ref):
        print "COMPUTE_SCORE HASN'T BEEN DEFINED"
        return -1

    def method(self):
        return "Bleu"

    def cook_append(self, test, refs):
        '''called by constructor and __iadd__ to avoid creating new instances.'''
        
        if refs is not None:
            self.crefs.append(cook_refs(refs))
            if test is not None:
                cooked_test = cook_test(test, self.crefs[-1])
                self.ctest.append(cooked_test) ## N.B.: -1
            else:
                self.ctest.append(None) # lens of crefs and ctest have to match

        self._score = None ## need to recompute

    def ratio(self, option=None):
        self.compute_score(option=option)
        return self._ratio

    def score_ratio(self, option=None):
        '''return (bleu, len_ratio) pair'''
        return (self.fscore(option=option), self.ratio(option=option))

    def score_ratio_str(self, option=None):
        return "%.4f (%.2f)" % self.score_ratio(option)

    def reflen(self, option=None):
        self.compute_score(option=option)
        return self._reflen

    def testlen(self, option=None):
        self.compute_score(option=option)
        return self._testlen        

    def retest(self, new_test):
        if type(new_test) is str:
            new_test = [new_test]
        assert len(new_test) == len(self.crefs), new_test
        self.ctest = []
        for t, rs in zip(new_test, self.crefs):
            self.ctest.append(cook_test(t, rs))
        self._score = None

        return self

    def rescore(self, new_test):
        ''' replace test(s) with new test(s), and returns the new score.'''
        
        return self.retest(new_test).compute_score()

    def size(self):
        assert len(self.crefs) == len(self.ctest), "refs/test mismatch! %d<>%d" % (len(self.crefs), len(self.ctest))
        return len(self.crefs)

    def __iadd__(self, other):
        '''add an instance (e.g., from another sentence).'''

        if type(other) is tuple:
            ## avoid creating new Bleu instances
            self.cook_append(other[0], other[1])
        else:
            assert self.compatible(other), "incompatible BLEUs."
            self.ctest.extend(other.ctest)
            self.crefs.extend(other.crefs)
            self._score = None ## need to recompute

        return self        

    def compatible(self, other):
        return isinstance(other, Bleu) and self.n == other.n

    def single_reflen(self, option="average"):
        return self._single_reflen(self.crefs[0][0], option)

    def _single_reflen(self, reflens, option=None, testlen=None):
        
        if option == "shortest":
            reflen = min(reflens)
        elif option == "average":
            reflen = float(sum(reflens))/len(reflens)
        elif option == "closest":
            reflen = min((abs(l-testlen), l) for l in reflens)[1]
        else:
            assert False, "unsupported reflen option %s" % option

        return reflen
        
    def compute_score_old(self, option=None, addprec=None):
        if self._score is not None:
            return self._score

        if option is None:
            option = "average" if len(self.crefs) == 1 else "closest"
        if addprec is None:
            addprec = 1 if len(self.crefs) == 1 else 0 ## automatic bleu+1
            
        n = self.n

        self._testlen = 0
        self._reflen = 0
        totalcomps = {'testlen':0, 'reflen':0, 'guess':[0]*n, 'correct':[0]*n}

        # for each sentence
        for comps in self.ctest:
            testlen = comps['testlen']
            self._testlen += testlen

            if self.special_reflen is None: ## need computation
                reflen = self._single_reflen(comps['reflen'], option, testlen)
            else:
                reflen = self.special_reflen

            self._reflen += reflen
                
            for key in ['guess','correct']:
                for k in xrange(n):
                    totalcomps[key][k] += comps[key][k]

        bleu = 1.
        small = 1e-9
        tiny = 1e-15 ## so that if guess is 0 still return 0
        for k in xrange(n): 
            bleu *= float(totalcomps['correct'][k] + addprec + tiny ) \
                    / (totalcomps['guess'][k] + addprec + small)
        bleu = bleu ** (1./n)

        ## smoothing: single-sentence effect on the whole doc
        ratio = (self._testlen + tiny) / (self._reflen + small) ## N.B.: avoid zero division
        if ratio < 1: #0 < totalcomps['testlen'] < totalcomps['reflen']:        
            bleu *= math.exp(1-1/ratio)

        self._score = bleu
        self._ratio = ratio
        return self._score


    ## real interface
    score = fscore = compute_score_old

def is_latin(s, lineid=0):
    try:
        s.decode('utf-8').encode('latin_1')
        return True
    except:
        print >> logs, "WARNING: non-latin word removed from line %d: %s" % (lineid, s)
        return False    

def remove_nonlatin(line, lineid=0):
    return " ".join(w for w in line.split() if is_latin(w, lineid))
#
# if __name__ == "__main__":
#     import itertools, fileinput
#
#     flags.DEFINE_integer("first", 100000, "first N sentences")
#
#     argv = FLAGS(sys.argv)
#
#     # infile = fileinput.input(argv[1]) # "-" OK
#     # reffilenames = argv[2:]
#
#     bleus = Bleu()
#
#     # ## STEP 0: READ IN TESTS
#     # testlines = []
#     # for i, line in enumerate(infile, 1):
#     #     testlines.append(line)
#     #     if i >= FLAGS.first:
#     #         break
#     # testlines = ['hello world']
#     # refs = [['h   ello']]
#     testlines = ['A person is riding a skateboard on a picnic table with a crowd watching.']
#     refs = [['The skateboarder is putting on a show using the picnic table as his stage.', 'A skateboarder pulling tricks on top of a picnic table.', 'A man riding on a skateboard on top of a table.', 'A skate boarder doing a trick on a picnic table.']]
#
#     # ## STEP 1: READ IN REFS
#     # refs = []
#     # for i, lines in enumerate(itertools.izip(*[file(filename) for filename in reffilenames]), 1):
#     #     refs.append(lines)
#     #     if i >= len(testlines) or i >= FLAGS.first:
#     #         break
#
#
#
#     ## STEP 2: COOK TESTS
#     for i, (testline, ref) in enumerate(zip(testlines, refs), 1):
#         if FLAGS.latin:
#             print 'do nothing'
#             # testline = remove_nonlatin(testline, i)
#         bleus += (testline, ref)
#
#     ## STEP 3: EVALUATE (with effective ref len)
#     bleu = bleus.fscore(option=FLAGS.eff_ref_len)
#     ratio = bleus.ratio()
#     print >> logs, "bleu%s = %.4lf, length_ratio = %.2lf (%d sentences, length option \"%s\", nist_tokenize: %s)" \
#           % ("+1" if bleus.size() == 1 else "", bleu, ratio, bleus.size(), FLAGS.eff_ref_len, FLAGS.nist_tokenize)