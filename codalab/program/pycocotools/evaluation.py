__author__ = 'tylin'
from shapely.geometry import Polygon
import numpy as np
def precision_and_recall(truths_list, dets_list):
    fps = 0
    tps = 0
    num_ts = 0
    for truths, dets in zip(truths_list, dets_list):
        det_th = 0.0
        op_th = 0.5
        iou_mat, det_vec = iou_truths_dets(truths, dets)
        fp, tp, num_t = hit_and_miss(iou_mat, det_vec, det_th, op_th)
        fps += fp
        fps += tp
        num_ts += num_t
    rec, prec = compute_score(fp, tp, num_t)
    print rec, prec
    return [rec, prec]


def iou_truths_dets(truths, dets):
    truths_polys = [anno2polys(anno) for anno in truths]
    dets_polys = [anno2polys(anno) for anno in dets]
    N = len(truths_polys)
    M = len(dets_polys)
    iou_mat = np.zeros((M,N))
    det_vec = np.zeros((M,))
    for m, d in enumerate(dets_polys):
        det_vec[m] = d['score']
        for n, t in enumerate(truths_polys):
            iou_mat[m,n] = d.intersection(t).area / d.union(t).area

    return [iou_mat, det_vec]

def hit_and_miss(iou_mat, det_vec, det_th, op_th):
    # TODO sorted by det score or iou
    ind = np.nonzero(det_vec>det_th)
    iou_mat = iou_mat.copy()
    iou_mat = iou_mat[ind,:]
    num_t = len(ind)
    fp = 0
    tp = 0
    for iou_row in iou_mat:
        ind = iou_row.argmax()
        if iou_row[ind] > op_th:
            tp += 1
            iou_mat = np.delete(iou_mat, ind, 1)
        else:
            fp += 1

    return [fp, tp, num_t]

def compute_score(fp, tp, num_t):
    rec = tp/num_t
    prec = tp / (fp+tp)
    return [rec, prec]

def anno2polys(anno):
    point_lists = anno['segmentation']
    polys = Polygon([])
    for pts in point_lists:
        poly = []
        for i in range(0, len(pts), 2):
            poly.append((pts[i], pts[i+1]))
        polys.union(Polygon(poly))
        # if len(polys) == 0:
        #     polys = Polygon(poly)
        # else:
        #     polys = polys.union(poly)
    return polys
