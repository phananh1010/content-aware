import numpy as np
import namespace
import cv2

class mAP:
    def __init__(self):
        return

    def calculate_box_area(self, _box):
        TL = _box[0], _box[1]
        BR = _box[2], _box[3]
        return self.check_order_topleft_botright(TL, BR)

    def get_full_coord_from_topleft_botright(self, _topleft, _botright):
        coord_X = _topleft
        coord_Y = _botright
        #X ~ WIDTH, Y ~ HEIGHT
        x1, y1, x2, y2 = coord_X
        x3, y3, x4, y4 = coord_Y
        A, B, C, D = (x1, y1), (x2, y1), (x2, y2), (x1, y2)
        E, F, G, H = (x3, y3), (x4, y3), (x4, y4), (x3, y4)
        return (A, B, C, D), (E, F, G, H)
    
    def calculate_overlap(self, _box1, _box2):
        #INPUT is (x1, y1, x2, y2), (x3, y3, x4, y4)
        #return overlap region
        (A, B, C, D), (E, F, G, H) = self.get_full_coord_from_topleft_botright(_box1, _box2)

        #Generate I, J, K, which are three points of the intersection box
        I = (max(A[0], E[0]), max(A[1], E[1]))#topleft
        J = (min(B[0], F[0]), max(A[1], E[1]))
        L = (min(D[0], H[0]), min(D[1], H[1]))
        K = (J[0], L[1])

        S = self.check_order_topleft_botright(I, K)
        return I, K, S

    def check_order_topleft_botright(self, _topleft, _botright):
        #check the order consistency of _topleft and _botright
        #return area created by _topleft, _botright
        d = np.array(_botright) - np.array(_topleft)
        if d[0] > 0 and d[1] > 0:
            return d[0] * d[1]
        else:
            return 0    
    
    def calculate_overlap(self, _box1, _box2):
        #INPUT is (x1, y1, x2, y2), (x3, y3, x4, y4)
        #return overlap region
        (A, B, C, D), (E, F, G, H) = self.get_full_coord_from_topleft_botright(_box1, _box2)

        #Generate I, J, K, which are three points of the intersection box
        I = (max(A[0], E[0]), max(A[1], E[1]))#topleft
        J = (min(B[0], F[0]), max(A[1], E[1]))
        L = (min(D[0], H[0]), min(D[1], H[1]))
        K = (J[0], L[1])

        S = self.check_order_topleft_botright(I, K)
        return I, K, S
    
    #calculate intersection over union
    def calculate_IOU(self, _box1, _box2):
        #TODO: calculate ratio of intersection over union
        #INPUT: two bouding box, each is a tuple of 4 values
        #OUTPUT: a real number
        TL, BR, S =  self.calculate_overlap(_box1, _box2)
        SA = self.calculate_box_area(_box1)
        SB = self.calculate_box_area(_box2)
        return S * 1.0 / (SA + SB - S)
    
   
    def match_bbox(self, _gt_obj, _pd_obj_list, _matched_pdobj_list):
        #filter out bbox less than threshold, 
        #return list of candidates, regardless of the class
        #format([0, class, confidence, h, w, dh, hw])
        #INPUT: one gt obj and a list of available prediction (specified by _matched_pdobj_list)
        #RETURN #false mean the algorithm failed to detect the gt obj or []?

        result = []
        for pd_obj in _pd_obj_list:
            #result is confidence (to sort), the pred item, the overlap)
            result.append([pd_obj[2], pd_obj, self.calculate_IOU(_gt_obj[3:], pd_obj[3:])])
        #list of sorted result, format = (confidence, pd_obj data, IOU), filter out IOU < .5
        result = sorted([item for item in result if item[2] >= namespace.THRESHOLD_IOU and tuple(item[1]) not in _matched_pdobj_list], key=lambda x: x[0], reverse=True)

        return result
    
    def step1_match_bbox(self, pd_obj_list, gt_obj_list):
        #
        #input: list of prediction for given frame, [[0, class, confidence, bbox]]
        # .    gt annotation for given frame        [[0, class, 1, bbox]]
        #return structure: a dict {gt_obj: [pd_obj]}, show pd_obj matched the gt_obj using match_bbox function
        result = {}
        matched_list = set()
        for gt_obj in gt_obj_list:
            gt_obj = tuple(gt_obj)
            if gt_obj not in result:
                result[gt_obj] = self.match_bbox(gt_obj, pd_obj_list, matched_list)
        return result
    
    def step2_sort_matchedbbox(self, _matched_bbox_dict, pd_obj_list, gt_obj_list):
        #TODO: sort all matched bbox buy decreasing confidence
        #input: matched_bbox_dict from step1. {gt_obj: [pd_obj]}
        #output format: (class gt, class pd, confidence, key). sorted by confidence.
        result = []
        for gt_obj in gt_obj_list:
            gt_obj = tuple(gt_obj)
            for item in _matched_bbox_dict[gt_obj]:
                #item is (confidence, [0, pd_class, conf, bbox], IOU)
                #class gt, class pd, confidence, gtobj_key
                result.append([gt_obj[1], item[1][1], item[0], tuple(gt_obj)])
        result = sorted(result, key=lambda x: x[2], reverse=True)#sort by confidence
        return result
    
    def step3_predict_on_sortedmatchedbbox(self, _sorted_matched_bboxlist, pd_obj_list, gt_obj_list):
        #TODO: create a precision list & a recall list to calculate the mAP curve
        #input: sorted matched bbox is bbox matched (iou > .5), sorted by confidence
        #              input format (class gt, class pd, confidence, gt_obj)
        #output: raw acc_list, raw recall_list. Raw means direct results for each sorted matched bbox
        
        #gt_obj_list = _annotation_dir_dict[_filetoken]
        pd_list = []
        expand_item_list = set()#list of gt item that have been considered, to prevent multiple pd_bbox point to same gt_bbox
        
        #first, compare the gt_class & predicted_class in sorted_matched_bboxlist to determine accuracy
        for item in _sorted_matched_bboxlist:
            if item[0] == item[1] and item[3] not in expand_item_list:
                pd_list.append(1)
                expand_item_list.add(item[3])
            elif item[0] == item[1] and item[3] in expand_item_list:
                pd_list.append(0)
            elif item[0] != item[1]:
                pd_list.append(0)
        
        #next, derive acc and rc list to calculate average precision
        n_objects = len(gt_obj_list)
        #from prediction list, create pr curve
        last1 = -1
        for idx,_ in enumerate(pd_list):
            if pd_list[idx] == 1:
                last1 = idx
        pd_list = pd_list[:last1+1]
        acc_list = [1.0] + [sum(pd_list[:i])*1.0/len(pd_list[:i]) for i in range(1, len(pd_list)+1)]
        rc_list = [0.0] + [sum(pd_list[:i])*1.0/n_objects for i in range(1, len(pd_list)+1)]
        
        return pd_list, acc_list, rc_list
    
    def step4_prcurve_from_accrclist(self, _acc_list, _rc_list):
        #TODO: create precision recall curve
        #input: acc_list (precision) & rc_list (recall) in previous step
        #output: 
        pr_dict = {item:[] for item in np.arange(0, 1, .1)}
        for item in pr_dict:
            for idx, rc in enumerate(_rc_list):
                if rc >= item: 
                    pr_dict[item].append(_acc_list[idx])
        for item in pr_dict:
            pr_dict[item] = sorted(pr_dict[item], reverse=True)

        result = []
        for item in pr_dict:
            prcs, rcal = item, pr_dict[item][0] if len(pr_dict[item]) > 0 else 0
            result.append([prcs, rcal])
        result = sorted(result, key=lambda x:x[0])

        #result is list of (prcs, rcal) points in the curve
        return result
    
    def map_from_prcurve(self, _pc_curve):
        return np.array(_pc_curve)[:, 1].mean()

    def score(self, pd_obj_list, gt_obj_list):
        #TODO: main entry to calculate mAP metric
        #input: array of predicted bbox, array of gt objects
        matched_bbox_dict = self.step1_match_bbox(pd_obj_list, gt_obj_list)
        sorted_matched_bbox = self.step2_sort_matchedbbox(matched_bbox_dict, pd_obj_list, gt_obj_list)
        pd_list, acc_list, rc_list = self.step3_predict_on_sortedmatchedbbox(sorted_matched_bbox, pd_obj_list, gt_obj_list)
        prcurve = self.step4_prcurve_from_accrclist(acc_list, rc_list)

        return self.map_from_prcurve(prcurve)
    
    def score_from_file(self, filepath, converter, predictor, anno):
        #ftoken = converter.get_token_from_filepath(filepath)
        #dtoken = converter.get_dirtoken_from_filetoken(ftoken)
        image = cv2.imread(filepath, cv2.IMREAD_COLOR)
        pred = predictor.detect(image)
        pred_item = converter.convert_prediction_item(pred)
        score =  self.score(pred_item, anno)
        
        return score