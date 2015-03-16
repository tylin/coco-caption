__author__ = 'tylin'

from pycocotools.coco import COCO
from pycocoevalcap.eval import COCOEavlCap
import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.3f')

dataDir='.'
dataType='val2014'
algName = 'fakecap'
annFile='%s/annotations/captions_%s.json'%(dataDir,dataType)
subtypes=['results', 'evalImgs', 'eval']
[resFile, evalImgsFile, evalFile]=['%s/results/captions_%s_%s_%s.json'%(dataDir,dataType,algName,subtype) for subtype in subtypes]

coco = COCO(annFile)
cocoRes = coco.loadRes(resFile)

cocoEval = COCOEavlCap(coco, cocoRes)
cocoEval.params['image_id'] = cocoRes.getImgIds()
cocoEval.evaluate()

json.dump(cocoEval.evalImgs, open(evalImgsFile, 'w'))
json.dump(cocoEval.eval,     open(evalFile, 'w'))