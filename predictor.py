import glob
import cv2
import namespace
import numpy as np
import torch as t

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
        detections = self._net(processed_tensor).data
        return detections