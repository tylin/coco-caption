from pycocoevalcap.bleu import bleu
from pycocoevalcap.cider import cider
from pycocoevalcap.meteor import meteor
from pycocoevalcap.rouge import rouge
from pycocoevalcap.spice import spice
import sys


def isclose(a, b, rel_tol=1e-5, abs_tol=1e-5):
    if isinstance(a, list):
        if not isinstance(b, list) or len(a) != len(b):
            return False
        return all([isclose(A,B) for A,B in zip(a,b)])
    else:
        return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


references = {
    0:['the cat in the hat is black .'],
    1:['unsurprisingly it was discovered out that most humans are insensitive to different shades of gray']
}

candidates = {
    0:['the black cat is hat is hat'],
    1:['humans are mostly insensitive to different colors except gray']
}

print ('Python version {}'.format(sys.version_info))

def test_metric(metric_object, true_score, references, candidates):
    score, score_vec = metric_object.compute_score(references, candidates)
    print('\ttrue (corpus) {}'.format(true_score))
    print('\tpredicted (corpus) {}'.format(score))
    print('\tpredicted (individual) {}'.format(score_vec))

    pass_test = isclose(score, true_score)
    if pass_test:
        print('[    OK    ]')
    else:
        print('[    FAIL    ]')
    return pass_test

print('References {}'.format(references))
print('Candidates {}'.format(candidates))

tests = [
   # ('Rouge', rouge.Rouge(), references, candidates, 0.5027146063609029),
    #('Bleu', bleu.Bleu(), references, candidates, [0.44388336186369043, 0.28615312506956214, 0.16393460357431763, 2.309415185245007e-05]),
    #('Cider', cider.Cider(), references, candidates, 1.55587810018),
    #('Meteor', meteor.Meteor(), references, candidates, 0.257030123779),
    #('Spice', spice.Spice(), references, candidates, 0.597222222222)
]


# Some additional tests
tests.append((
    'Cider 2',
    cider.Cider(),
    # ref
    {
        1: ['dog runs'],
        2: ['dog will hunt'],
    },
    { # cand
        1: ['dog walks'],
        2: ['dog will hunt'],
    },
    3.75
))

# Some additional tests
tests.append((
    'Bleu 2',
    bleu.Bleu(),
    # ref
    {
    1:['here is a test of bleu',
    'here is a test of blue'],
    2:['please worry it probably wont pass',
    'dont worry it will probably pass'],
    },
    {
        1: ['this is a test of bleu'],
        2: ['dont worry it will probably pass'],
    },
    [0.9166666665138891, 0.9082951060702961, 0.8970582964112459, 0.8806841673159312]
))

tests.append((
    'Meteor 2',
    cider.Cider(),
    # ref
    {
        1: ['i did a test'],
        3: ['strain pot after waiting eight minutes for the pasta'],
        2: ['cooking is a fun activity, so give it a try.']
    },
    { # cand
        1: ['this is a test'],
        2: ['cooking can be quite fun, if you give it a chance.'],
        3: ['wait eight minutes, and then strain the contents of the pot.']
    },
    1.35741235571
))

tests.append((
    'Rouge-L 2',
    rouge.Rouge(),
    # ref
    {
        'string_key': ['this is a strange key', 'one more, to throw you off'],
        1: ['THIS.              is     !a dog     ,at the PaRK.'],
    },
    {
        'string_key': ['this is a strange key'],
        1: [' this. is! a doG, at the parK .'],
    },
    0.549472830495
))



results = []
for metric_name, metric_object, ref, cand, true_score in tests:
    print ('\n{}'.format(metric_name))
    pass_test = test_metric(metric_object, true_score, ref, cand)
    results.append(pass_test)

if all(results):
    print('\nAll tests have PASSED')
else:
    print('\nSome tests have FAILED')