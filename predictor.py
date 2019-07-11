import glob
import cv2
import namespace
import numpy as np
import torch as t

import utils

from ssd import ssd
from ssd.data import VOC_CLASSES as labels


class Predictor(object):
    def __init__(self):
        self._net = ssd.build_ssd('test', 300, 21)
        self._net.load_weights(namespace.FILEPATH_SSD_WEIGHT )
        return
    
    def preprocess(self, image):
        x = cv2.resize(image, (300, 300)).astype(np.float32)
        x -= (104.0, 117.0, 123.0)
        x = x.astype(np.float32)
        x = x[:, :, ::-1].copy()
        x = t.from_numpy(x).permute(2, 0, 1)

        xx = t.autograd.Variable(x.unsqueeze(0))     # wrap tensor in Variable
        if t.cuda.is_available():
            xx = xx.cuda()

        return xx
    
    def detect(self, image):
        #sample data: './VID_data/ILSVRC2015_VID_train_0000/ILSVRC2015_train_00003000/000461.JPEG'
        #two step: convert image to tensor, then predict using ssd model
        processed_tensor = self.preprocess(image)
        detection0 = self._net(processed_tensor).data
        detections = self.convert_prediction_item(detection0)
        return detections
    
    def convert_prediction_item(self, predictions, threshold_confidence=namespace.THRESHOLD_CONFIDENCE):
        #TODO: convert raw prediction tensor from ssd model into customized structure used in mAP measurement
        #input: prediction from SSD model for ONE video frame, tensor shape (1, 21, 200, 4)
        #output: format that will allow calculating mAP {frame_token: [[0, customed_idx_class, confidence, hi, wi, dh, dw]]}
        #step 1: convert shape (1, 21, 200, 4) to a list of [0, VOC_idx_class, confidence, hi, wi, dh, dw]
        #step 2: convert [0, VOC_idx_class, confidence, hi, wi, dh, dw] into 
        
        result = []
        _, n_objclass, n_bbox, _ = predictions.shape
        for idx_vocobj in range(n_objclass):
            for idx_bbox in range(n_bbox):
                score = float(predictions[0, idx_vocobj, idx_bbox, 0].numpy())
                if score < threshold_confidence:
                    continue
                #final steps: convert VOC id to customized id
                idx_class = utils.convert_VOC_CLASSID_to_CLASSID(idx_vocobj)
                if idx_class == None:
                    #print 'FAILED: ', idx_bbox, idx_vocobj
                    continue
                hi, wi, dh, dw = predictions[0, idx_vocobj, idx_bbox, 1:].numpy()
                result.append([0, idx_class, score, hi, wi, dh, dw])

        
        return result