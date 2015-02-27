__author__ = 'tylin'

import json
def pack_coco_annotations(ann_file):
    '''
    Pack COCO annotations for evaluation code.
    :param ann_file: COCO annotations file to load
    :return: dictionary for evaluation code
    '''
    anns = json.load(open(ann_file))
    if not 'annotations' in anns:
        print '"annotations" in the JSON file.'
        raise
    anns = anns['annotations']

    # pack output dictionary
    dict = {}
    for ann in anns:
        if not ann['image_id'] in dict:
            dict[ann['image_id']] = []
        dict[ann['image_id']].append(ann['caption'])
    return dict

def pack_coco_submission(submission_file):
    '''
    Pack COCO submission for evaluation code.
    :param ann_file: COCO submission file to load
    :return: dictionary for evaluation code
    '''
    anns = json.load(open(submission_file))

    # pack output dictionary
    dict = {}
    for ann in anns:
        if not ann['image_id'] in dict:
            dict[ann['image_id']] = []
        dict[ann['image_id']].append(ann['caption'])
    return dict
