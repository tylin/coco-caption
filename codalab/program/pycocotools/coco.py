__author__ = 'tylin'
__version__ = 0.9
import json
import datetime
import itertools
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pylab
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import numpy as np

class COCO:
    def __init__(self, annotation_file='annotations/instances_train2014a.json', image_folder='./images'):
        """
        Constructor of Microsoft COCO helper class for reading and visualizing annotations.
        :param annotation_file: string location of annotation file
        :param image_folder: string location to the folder that hosts images.
        :return:
        """
        # load dataset
        print 'loading annotations into memory...'
        time_t = datetime.datetime.utcnow()
        dataset = json.load(open(annotation_file, 'r'))
        print datetime.datetime.utcnow() - time_t
        print 'annotations loaded!'

        ann_key = ''
        # set up annotation types
        if 'instances' in dataset.keys():
            ann_key = 'instances'
        elif 'sentences' in dataset.keys():
            ann_key = 'sentences'

        time_t = datetime.datetime.utcnow()
        # create index
        print 'creating index...'
        image_to_annotations = {ann['image_id']: [] for ann in dataset[ann_key]}
        annotations =          {ann['id']:       {} for ann in dataset[ann_key]}
        for ann in dataset[ann_key]:
            image_to_annotations[ann['image_id']] += [ann]
            annotations[ann['id']] = ann
        images = {im['id']: {} for im in dataset['images']}
        for im in dataset['images']:
            images[im['id']] = im

        categories = []
        if ann_key == 'instances':
            categories = {cat['id']: [] for cat in dataset['categories']}
            for cat in dataset['categories']:
                categories[cat['id']] = cat

        print datetime.datetime.utcnow() - time_t
        print 'index created!'

        # create class members
        self.annotations = annotations
        self.ann_key = ann_key
        self.image_to_annotations = image_to_annotations
        self.images = images
        self.image_folder = image_folder
        self.dbinfo = dataset['info']
        self.categories = categories


    def info(self):
        """
        Print information about the annotation file.
        :return:
        """
        for key, value in self.dbinfo.items():
            print '%s: %s'%(key, value)

    def getImageIds(self, params={}):
        """
        Get image IDs from annotations.  One can use params to get filtered results.
        :param params: { 'cat_id: int'}
                        Filter images that contain specified object category.
                        If params is empty, return all image IDs in the dataset.
        :return: a list of image IDs
        """
        # load all images if no constraint specified
        if params == {}:
            return self.images.keys()
        # get instances with filtering constraints
        im_id_lists = []
        # specific filtering for instances annotations
        if self.ann_key == 'instances' and 'cat_id' in params.keys():
            im_id_lists.append( [ann['image_id'] for ann_id, ann in self.annotations.items() if ann['category_id'] == params['cat_id']] )
        # aggregate the queries by AND operation
        if len(im_id_lists) == 0:
            im_id_list = []
        for i, l in enumerate(im_id_lists):
            assert isinstance(l, list)
            im_id_list = set(im_id_list) & set(l) if not i == 0 else set(l)
        return list(im_id_list)

    def loadAnnotations(self, params = {}):
        """
        Get instance annotations.  One can use params to get filtered results.
        :param params: {'im_id_list': list(int),    # instances are in the list of images
                        'cat_id': int,              # instances with specified category
                        'area__lt': float,          # instances have pixel area less than the number
                        'area__gt': float,          # instances have pixel area greater than the number
                        }
                        Params is used to filter instance annotations.
                        The output is the intersection of output from all constraints.
                        If params is empty, return all annotation instances in the dataset.
        :return: list of instance objects
        """
        # load all instances if no constraint specified
        if params == {}:
            return [ ann for ann_id, ann in self.annotations.items() ]
        # get instances with filtering constraints
        ins_id_lists = []
        # universal filtering params for all types of annotations
        if 'im_id_list' in params.keys():
            ins_id_lists.append( [ x['id'] for x in
                                   (itertools.chain(
                                       *[self.image_to_annotations[im_id] for im_id in params['im_id_list'] if im_id in self.image_to_annotations]
                                   ))
            ])
        # specific filtering for instances annotations
        if self.ann_key == 'instances' and 'cat_id' in params.keys():
            ins_id_lists.append( [ann_id for ann_id, ann in self.annotations.items() if ann['category_id'] == params['cat_id']] )
        if self.ann_key == 'instances' and 'area__lt' in params.keys():
            ins_id_lists.append( [ann_id for ann_id, ann in self.annotations.items() if ann['area'] < params['area__lt']] )
        if self.ann_key == 'instances' and 'area__gt' in params.keys():
            ins_id_lists.append( [ann_id for ann_id, ann in self.annotations.items() if ann['area'] > params['area__gt']] )
        # aggregate the queries by AND operation
        if len(ins_id_lists) == 0:
            ins_id_list = []
        for i, l in enumerate(ins_id_lists):
            assert isinstance(l, list)
            ins_id_list = set(ins_id_list) & set(l) if not i == 0 else set(l)
        return [ self.annotations[ins_id] for ins_id in ins_id_list ]

    def showAnns(self, anns, MAX_IMAGE_TO_SHOW=10):
        """
        Visualize annotations.
        :param anns: the list of instance annotations to be visualized.  The instances in the same image will be shown in the same figure.
        :param MAX_IMAGE_TO_SHOW: The maximum number of images to visualize.  This can prevent showing too many images.
        :return:
        """
        # group anns by images
        im_id_list = list(set([ann['image_id'] for ann in anns]))
        for im_id in im_id_list[0:MAX_IMAGE_TO_SHOW]:
            im = self.loadImage(im_id)
            plt.imshow(im)
            ax = plt.gca()
            # loop through all annotations
            for ann in anns:
                if not ann['image_id'] == im_id:
                    continue
                # show instances annotation
                if self.ann_key == 'instances':
                    polygons = []
                    for seg in ann['segmentation']:
                        poly = np.array(seg).reshape((len(seg)/2, 2))
                        polygons.append(Polygon(poly, True))
                    color = np.random.random((1, 3))
                    p = PatchCollection(polygons, facecolors=color, edgecolors=(0,0,0,1), linewidths=3, alpha=0.4)
                    ax.add_collection(p)
                # show sentences
                if self.ann_key == 'sentences':
                    print ann['sentence']
            pylab.show()

    def loadImage(self, im_id):
        """
        Load images with image objects.
        :param im: a image object in input json file
        :return:
        """
        im = self.images[im_id]
        return mpimg.imread(open('%s/%s/%s'%(self.image_folder, im['file_path'], im['file_name']), 'r'))