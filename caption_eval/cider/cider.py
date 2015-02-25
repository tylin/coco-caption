# Filename: cider.py
#
# Description: Describes the class to compute the CIDEr Metric
#
# Creation Date: Sun Feb  8 14:16:54 2015
#
# Author: Ramakrishna Vedantam
#
# Note: Make sure that the pre-processing script preprocessing_cider.py is run prior to running this script
#       That script runs preprocessing on reference sentences, which are used in this script
#
# TODO: 1. Implement Stemming 
#       2. Fix Brevity Penalty issues

import numpy as np
import pickle
from itertools import chain
from scipy.sparse import csr_matrix
from collections import defaultdict, Counter
import pdb


def split_tokens(corpus):
    """
    Split each sentence for an image into a collection of words

    Parameters
    -----------------
    corpus: dict with key = image and value = sentences for the image

    Returns
    -----------------
    corpus: dict with key = image and value = each sentence for an image 
                            split into a list of words

    Notes
    -----------------
    Python does in essense, call by reference so does not need a return 
    statement

    See Also
    -----------------
    """
    for image in corpus:
        for i, sentence in enumerate(corpus[image]):
            corpus[image][i] = corpus[image][i].split(' ')

    return corpus

def get_ngrams(sentence, ngrams):
    """
    Given a sentence, generate all the ngrams of the specified length

    Parameters
    ------------------
    sentence: list of str

    ngrams: int 

    Returns
    ------------------
    list containing n-grams of length "n"

    Notes
    ------------------

    See Also
    ------------------
    """
    return zip(*[sentence[i:] for i in range(ngrams)])

def index_words(tokens, ngrams = 1):
    """
    Compute a dictionary from reference tokens for various n-gram sizes

    Parameters
    ------------------
    tokens: list (for all images)
                of
                    list (for all sentences for an image)
                        of 
                            list (for each sentence)
    ngrams: int

    Returns
    ------------------
    dictionary: list (for n = 1 to ngrams)
                    of
                        dict (key: words/ngrams value:indexing id)

    Notes
    ------------------

    See Also
    ------------------

    """
    dictionary = []
    for ng in range(1, ngrams+1):
        flat_tokens = [item for sublist in tokens for item in get_ngrams(sublist, ng)]
        word_dict = {}
        for i, w in enumerate(list(set(flat_tokens))):
            word_dict[w] = i
        dictionary.append(word_dict);
    return dictionary

def concatenate(items):
    """
    Conflate a list of lists into a list

    Parameters
    -------------------
    items: list of list

    Returns
    -------------------
    new_items: list

    """
    new_items = []
    for i in items:
        new_items = new_items + i
    return new_items

def ngrams_to_vectors(corpus, dictionary, ngrams=1):
    """
    Given a dictionary, project a sentence into a vector space indexed by the dictionary

    Parameters
    -------------------
    corpus: dict (indexed by image)
                of 
                    list of str (sentences)
    dictionary: list (for n = 1 to ngrams)
                    of
                        dict (key: words/ngrams value:indexing id)
    ngrams: int

    Returns
    -------------------
    vector_ngrams: dict (idexed by image)
                        of
                            list (indexed by ngrams)
                                of scipy.sparse.csr_matrix
    Notes
    -------------------

    See Also
    -------------------
    """
    assert(ngrams < 5)

    vector_ngrams = {} 
    for i, image in enumerate(corpus):
        vector_ngrams[image] = []
        for n in range(1,ngrams+1):
            corpus_vec = []
            dictionary_n = dictionary[n-1]
            for sentences in corpus[image]:
                corpus_vec.append(dict_mul\
                    (Counter(get_ngrams(sentences,n)),dictionary_n));
            vector_ngrams[image].append(corpus_vec)
            print "Processed n = %d and image %d\n" % (n,i)        
    return vector_ngrams

def dict_mul (smaller_dict, dictionary):
    """
    Given a smaller dictionary, and indexing information into a larger dictionary, modify the
    larger dictionary with values from the smaller dictionary

    Parameters
    -------------------
    smaller_dict: dict with key = word/ngram and some value

    dictionary: dict with key = word/ngram and value = index for a word

    Returns
    -------------------
    vector of type scipy.sparse.csr_matrix of length equal to the size of larger dictionary

    Notes
    -------------------

    See Also
    -------------------
    """
    vect = [0]*len(dictionary) 
    for k,v in smaller_dict.items():
        if k in dictionary:
            vect[dictionary[k]] = v;
    return csr_matrix(vect, dtype=np.int16)

def compute_idf(words, ref, ngrams = 1):
    """
    Function to compute IDF given words forming a dictionary, and a refernece corpus_vecs

    Parameters
    -------------------
    words: list (for n = 1 to ngrams)
                of
                   dict (key: words/ngrams value:indexing id)
    corpus: dict (indexed by image)
                of 
                  list of str (sentences)
    ngrams: int

    Returns
    -------------------
    idfs: list (ngrams)
                of 
                    list of float

    Notes
    -------------------
    IDF values are computed using [log(num_of_documents/document_frequency)]

    See Also
    -------------------

    """
    idfs = []

    for ng in range(1,ngrams+1):
        dictionary_n = words[ng-1]

        idf= [0]*len(dictionary_n);
        # iterate over all the images
        for image in ref:
            ngrams_for_image = []
            for sent in ref[image]:
                ngrams_for_image = ngrams_for_image + get_ngrams(sent,ng)
            ngrams_for_image = set(ngrams_for_image)
            # after obtaining all ngrams for an image, check if it exists in dictionary and update
            for key in ngrams_for_image:
                if key in dictionary_n:
                    idf[dictionary_n[key]] = idf[dictionary_n[key]] + 1
        # ensure that each ngram occurs atleast once
        assert(0 not in idf)
        # convert document frequencies to IDF, with rounding
        idf = [round(np.log10(len(ref)/item),4) for item in idf]
        idfs.append(idf)

    return idfs

class Cider:
    """
    Main Class to compute the CIDEr metric described at : http://arxiv.org/abs/1411.5726

    """
    def __init__(self):
        self.ngrams = 4

    def score_cider(self, test_vec, ref_vecs, idf, ngrams = 1):
        """
        Compute CIDEr metric for a given image, using test sentences and reference sentences for that image

        Parameters:
        -----------------
        test_vec: list (ngrams)
                        of scipy.sparse.csr_matrix

        ref_vecs: list (ngrams)
                        of list (sentences)
                            of scipy.sparse.csr_matrix

        idfs: list (ngrams)
                    of 
                        list of float
        ngrams: int

        Returns:
        -----------------
        mean(score): where score is a list of n-gram CIDEr scores

        Notes:
        -----------------
        Need to correct for the Brevity Penalty issue (TODO)

        See Also:
        -----------------

        """
        score = []

        for ng in range(1,ngrams+1):
            idf_n = np.array(idf[ng-1])
            # only one test/candidate per image
            assert(len(test_vec[ng-1])==1)
            test_n = test_vec[ng-1][0]
            test = np.array(test_n.todense())
            # multiply with IDF
            test = idf_n*test

            score_n = []
            for ref_vec in ref_vecs[ng-1]:
                # multiply with IDF
                ref = np.array(ref_vec.todense())
                ref = ref*idf_n
                assert(len(ref[0])==len(test[0]))
                # compute cosine similarity
                score_n.append(ref[0].dot(test[0])/(np.linalg.norm(ref[0])*np.linalg.norm(test[0])))
                if np.isnan(score_n[-1]):
                    score_n[-1] = 0
                assert(score_n[-1]<=1+10**-6)
            score.append(np.mean(score_n))

        return np.mean(score)

    def compute_score(self, test, ref):
        """
        Compute the cider score given a reference dataset and test captions 
        """
        # preprocess test and ref to split into "tokens"
        split_tokens(test)

        # Obtain the n-gram dictionary from reference sentences
        words = pickle.load(open('data/words_ref.p','r'))
        idf = pickle.load(open('data/idf_ref.p','r'))

        # Project the reference and test tokens into the ngram vector space
        test_vecs = ngrams_to_vectors(test, words, ngrams=self.ngrams)
#        test_vecs = pickle.load(open('test_vec.p','r'))
        ref_vecs = pickle.load(open('data/ref_vecs.p','r'))
        scr_cider = []

        k = 0
        for image in test_vecs:
            scr_cider.append(self.score_cider(test_vecs[image], ref_vecs[image], idf, self.ngrams))
            print "scored CIDEr for image %d" % k
            k += 1
        return np.mean(scr_cider) 

    def method(self):
        return "CIDEr"