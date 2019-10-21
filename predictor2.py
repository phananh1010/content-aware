#NOTE: the predictor2.py replaces predictor.py. The Github project from predictor2.py support ssd300 and 500

import torch as t
from PIL import Image
import yacs
import glob
import os
import time
import numpy as np
import random
import copy

import namespace

from ssd2.ssd.data.transforms import build_transforms
from ssd2.ssd.modeling.detector import build_detection_model
from ssd2.ssd.utils.checkpoint import CheckPointer


HOME = '/home/u9167/testing/ssd2'
HOME_WEIGHTS = HOME + '/' + 'weights'
HOME_CONFIG = HOME + '/' + 'configs'
HOME_OUTPUTS = HOME + '/' + 'outputs'
MODELW_VOC300 = 'vgg_ssd300_voc0712.pth'
MODELW_VOC512 = 'vgg_ssd512_voc0712.pth'

CLASSNAME_VOC = ('__background__',
                   'aeroplane', 'bicycle', 'bird', 'boat',
                   'bottle', 'bus', 'car', 'cat', 'chair',
                   'cow', 'diningtable', 'dog', 'horse',
                   'motorbike', 'person', 'pottedplant',
                   'sheep', 'sofa', 'train', 'tvmonitor')#VOC_CLASS_DICT

CONFIG_SSD300 = HOME_CONFIG + '/' + 'vgg_ssd300_voc0712.yaml'
CONFIG_SSD512 = HOME_CONFIG + '/' + 'vgg_ssd512_voc0712.yaml'

OUTPUT_DIR_SSD300 = HOME_OUTPUTS + '/' + 'vgg_ssd300_voc0712'
OUTPUT_DIR_SSD512= HOME_OUTPUTS + '/' + 'vgg_ssd512_voc0712'
class Predictor(object):
    def __init__(self, version):
        #TODO: 
        #initialize variables
        #initialize model, 

        import ssd2.ssd.config
        if version == '300':
            ckpt = HOME_WEIGHTS + '/' + MODELW_VOC300
            config_file = CONFIG_SSD300
        elif version == '512':
            ckpt = HOME_WEIGHTS + '/' + MODELW_VOC512
            config_file = CONFIG_SSD512
        else:
            raise
        #NOTE: they use global object inside config.cfg, must use deepcopy to evade this problem
        cfg = copy.deepcopy(ssd2.ssd.config.cfg)
        cfg.merge_from_file(config_file)
        cfg.freeze()
           
        score_threshold=0.7
        images_dir='demo'
        output_dir = 'demo/result'
        dataset_type="voc"
        class_names = CLASSNAME_VOC
        device = t.device('cpu')

        model = build_detection_model(cfg)
        model = model.to(device)
        checkpointer = CheckPointer(model, save_dir=cfg.OUTPUT_DIR)
        checkpointer.load(ckpt, use_latest=ckpt is None)
        weight_file = ckpt if ckpt else checkpointer.get_checkpoint_file()
        model.eval()
        
        transforms = build_transforms(cfg, is_train=False)
                
        self._device = device
        self._model = model
        self._cfg = cfg
        self._weight_file = weight_file
        self._transforms = transforms
        return
    
    
    def detect(self, image, threshold_confidence=0.7):#namespace.THRESHOLD_CONFIDENCE):
        #sample data: './VID_data/ILSVRC2015_VID_train_0000/ILSVRC2015_train_00003000/000461.JPEG'
        #two step: convert image to tensor, then predict using ssd model
        #image_name = os.path.basename(image_path)
        #image = np.array(Image.open(image_path).convert("RGB"))
        with t.no_grad():
            height, width = image.shape[:2]
            images = self._transforms(image)[0].unsqueeze(0)

            result = self._model(images.to(self._device))[0]

            result = result.resize((width, height)).to(self._device).numpy()
            boxes, labels, scores = result['boxes'], result['labels'], result['scores']
            
            #indices = scores > threshold_confidence
            #boxes, labels, scores = boxes[indices], labels[indices], scores[indices]
            result = self.convert_prediction_item(image, (boxes, labels, scores))
            
            return result
    
    def convert_prediction_item(self, image, predictions, threshold_confidence=namespace.THRESHOLD_CONFIDENCE):
        #NOTE: width ~ hi ~ x
        with t.no_grad():
            height, width = image.shape[:2]
            boxes, labels, scores = predictions 
            
            result = []
            for idx, _ in enumerate(boxes):
                score, idx_class_voc, (x1, y1, x2, y2) = scores[idx], labels[idx], boxes[idx]
                #NOTE: need to convert idx_class_voc to idx_class
                idx_class = idx_class_voc
                
                if score < threshold_confidence:
                    continue
                hi, wi, dh, dw = x1, y1, x2, y2#x2 - x1, y2 - y1
                hi, wi, dh, dw = hi*1.0/width, wi*1.0/height, dh*1.0/width, dw*1.0/height
                result.append([0, idx_class, score, hi, wi, dh, dw])
            return result