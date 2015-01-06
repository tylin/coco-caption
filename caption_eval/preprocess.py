__author__ = 'tylin'

import re, xml.sax.saxutils

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
    s = s.lower()         # this might not be identical to the original
    for (pattern, replace) in normalize2:
        s = re.sub(pattern, replace, s)
    return s.split()

def normalize_captions(obj):
    '''
    Normalize sentence in json object
    :param obj: json object.  contains keys (image_ids) and values (single or list of sentences)
    :return: normalize obj.  sentence is tokenized as a list of token
    '''
    for key, val in obj.items():
        if type(val) is list:
            obj[key] = map(normalize, map(str, val))
        else:
            obj[key] = normalize(str(val))
    return obj