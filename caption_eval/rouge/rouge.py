#!/usr/bin/env python
# 
# File Name : rouge.py
#
# Description : Computes ROUGE-L metric as described by Lin and Hovey (2004)
#
# Usage :
#
# Creation Date : 07-01-2015
# Author : Ramakrishna Vedantam

# TO-DO : Verify this implementation based on Original Author's Perl Code
def my_lcs(string, sub):
    """
    Calculates longest common subsequence for a pair of tokenized strings

    Parameters
    ----------------
    string : list of str
           tokens from a string split using whitespace
    sub : list of str
           shorter string, also split using whitespace

    Returns
    -----------
    length : list of int
           Length of the longest common subsequence between the two strings

    Notes
    --------
    my_lcs only gives length of the longest common subsequence, not the actual LCS
    """
    if(len(string)< len(sub)):
		sub, string = string, sub

    lengths = [[0 for i in range(0,len(sub)+1)] for j in range(0,len(string)+1)]

    for j in range(1,len(sub)+1):
		for i in range(1,len(string)+1):
			if(string[i-1] == sub[j-1]):
				lengths[i][j] = lengths[i-1][j-1] + 1
			else:
				lengths[i][j] = max(lengths[i-1][j] , lengths[i][j-1])

    return lengths[len(string)][len(sub)]

class Rouge():
    '''
    Object for computing ROUGE-L score for a set of candidate sentences for the MS COCO test set

    '''
    def __init__(self):
    	# verify the value of beta - not final yet
        # updated the value below based on discussion with Hovey
        self.beta = 1.2

    def compute_score(self, test, ref):
        """
        Computes Rouge-L score given a set of reference and candidate sentences for the dataset
        Invoked by evaluate_captions.py 

        Parameters
        ----------------
        test: dictionary 
              candidate / test sentences with "image name" key and "tokenized sentences" as values 
        ref: dictionary
              reference MS-COCO sentences with "image name" key and "tokenized sentences" as values

        Returns
        ----------------
        score: list of float
               mean ROUGE-L score computed by averaging scores for all the images 

        See also
        ----------------
        self.calc_score()

        Notes
        ----------------

        """
        score = [];
        for image in test:
   		   score.append(self.calc_score(test[image], ref[image]))

        self.score = sum(score)/float(len(score))
        return self.score

    def calc_score(self, candidate, refs):
        """
        Compute ROUGE-L score given one candidate and references for an image

        Parameters
        ---------------
        candidate: str
               candidate sentence to be evaluated
        refs: list of str
               COCO reference sentences for the particular image to be evaluated

        Returns
        ---------------
        score: int
            ROUGE-L score for the candidate evaluated against references

        Notes
        ---------------
        beta = 2 used as of now. Need to confirm if that is the appropriate value to use.

        """
        assert(len(candidate)==1)	
        assert(len(refs)>0)         
        prec = []
        rec = []

        # split into tokens and remove full stop
        token_c = candidate[0].split(" ")
        filter(lambda x: x !='.', token_c)
    	
        for reference in refs:
   		   # split into tokens and remove full stop
   		   token_r = reference.split(" ")
   		   filter(lambda x: x !='.', token_r)
   		   # compute the longest common subsequence
   		   lcs = my_lcs(token_r, token_c)
   		   prec.append(lcs/float(len(token_c)))
   		   rec.append(lcs/float(len(token_r)))

        prec_max = max(prec)
        rec_max = max(rec)

        if(prec_max!=0 and rec_max !=0):
   		   score = ((1 + self.beta**2)*prec_max*rec_max)/float(rec_max + self.beta**2*prec_max)
        else:
   		   score = 0.0
        return score

    def method(self):
        return "Rouge"
