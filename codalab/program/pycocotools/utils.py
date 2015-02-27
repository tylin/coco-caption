__author__ = 'tylin'
# code was modified from M. Maire
# https://github.com/mmaire/hsa-app/blob/dev/webapp/client/static/javascript/util/arr_util.js
import numpy as np
from skimage.draw import polygon
import matplotlib.pyplot as plt
import time

def rleCompress(arr):
    '''

    :param arr:
    :return:
    '''
    #default to preserving array type
    #count number of unique element runs in array
    N = len(arr)
    vals_list = []
    counts_list = []
    vals_list.append(arr[0])
    counts_list.append(1)
    pos = 0
    diffs = np.logical_xor(arr[0:N-1], arr[1:N])
    for n, diff in enumerate(diffs):
        if diff:
            pos +=1
            vals_list.append(arr[n+1])
            counts_list.append(1)
        else:
            counts_list[pos] += 1
    rle = {'size':      N,
           'vals':      np.array(vals_list, dtype=np.uint8),
           'counts':    np.array(counts_list) ,
           }

    return rle


 # Decompress run-length encoded (RLE) array.

def rleDecompress(rle):
    '''

    :param rle:
    :return:
    '''
    N = len(rle['vals'])
    arr = np.zeros( (rle['size'], ))
    n = 0
    for pos in range(N):
        for c in range(rle['counts'][pos]):
            rle['counts'][pos]
            arr[n] = rle['vals'][pos]
            n += 1
    return arr

def poly2mask(polys, imshape, bbox):
    img = np.zeros((imshape[0], imshape[1]), dtype=np.bool)
    img_crop = np.zeros((bbox[3]-bbox[1], bbox[2]-bbox[0]), dtype=np.bool)
    for poly in polys:
        poly = np.array(poly)
        x = poly[0::2] - bbox[0]
        y = poly[1::2] - bbox[1]
        rr, cc = polygon(y, x, img_crop.shape)
        img_crop[rr, cc] = True
    img[bbox[1]:bbox[3], bbox[0]:bbox[2]] = img_crop
    # plt.imshow(img)
    # plt.show()
    print np.sum(img)
    return img
polys = np.array(([[14.75, 255.61, 49.16, 217.52, 196.63, 219.98, 272.82, 226.12, 278.96, 210.14, 306.0, 216.29, 308.46, 228.58, 330.58, 223.66, 351.47, 210.14, 368.67, 226.12, 580.05, 240.87, 604.63, 301.08, 605.86, 317.06, 609.54, 313.37, 609.54, 442.41, 554.24, 476.82, 356.39, 495.25, 301.08, 495.25, 278.96, 505.08, 244.55, 491.57, 238.41, 487.88, 66.36, 454.7, 7.37, 420.29, 1.23, 346.55, 17.2, 344.1]]))
mask = poly2mask(polys, [600,700], [1, 210, 1+609, 210+295])

t = time.time()
rle = rleCompress(mask.reshape(600*700))
print time.time()-t
arr = rleDecompress(rle)
plt.imshow(arr.reshape((600,700)))
plt.show()

# arr = np.array([1.,0.,0.,0.,0.,1.,1.,1.,1.,0.,1.,0.])
# rle = rleCompress(arr)
# arr_new = rleDecompress(rle)
# print arr
# print rle['vals']
# print rle['counts']
# print arr_new