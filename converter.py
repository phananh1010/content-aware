import namespace
import copy
import re

class Converter(object):
    #two main functionality: 
    #1. convert raw annotation to customed annotation
    #2. convert ssd prediction to customed annotation
    #
    #the format of customed annotation is: 
    def __init__(self):
        return
    
    
    #some private and popular function, let it be static
    @staticmethod
    def get_ftoken_from_vidname_and_idx(_vid_dirdict, _vidname, _idx):
        #TODO: create unique file token from video names and index of image. 
        #        This is helpful to parse result from script files
        #INPUT: _vid_dirdict is dirtoken indexed by video named. This is possible since vidname<->ftoken is 1 to 1 mapping
        #       _vidname is name of the video
        #       _idx is index of the frame in video (sorted by name)
        dirtoken = _vid_dirdict[_vidname]
        
        return dirtoken + '_{0:06d}'.format(_idx)
    
    @staticmethod
    def get_token_from_filepath(_filepath):
        #input: MUST be path to vid frame (.jpg), not videos (.mp4)
        return '_'.join(re.split('\.|/', _filepath)[-4:-1])
    
    
    @staticmethod
    def get_dirtoken_from_vidpath(_vidpath):
        #input: must be path to video file (.mp4)
        return '_'.join(re.split('\.|/', _vidpath)[-3:-1])
    
    @staticmethod
    def get_dirtoken_from_filetoken(_file_token):
        #input: a token for a frame or a file. 
        #output: a token for a video or a directory containing those input frame
        #example input: ILSVRC2015_VID_train_0000_ILSVRC2015_train_00119016_000009
        #example output: ILSVRC2015_VID_train_0000_ILSVRC2015_train_00119016
        return '_'.join(_file_token.split('_')[:-1])
    
    #First functionality, convert raw imagenet ground truth annotation to customed
    
    def convert_IMAGENET_CLASSID_to_CLASSID(self, _id):
        #NOTE: VID stand for IMAGE VID dataset
        #TODO: convert ImageNet ID into our customed Class ID
        #example: 'n02691156' --> 1
        if namespace.VID_CLASS_DICT[_id] in namespace.CLASS_LIST:
            return namespace.CLASS_DICT[namespace.VID_CLASS_DICT[_id]]
        else: 
            return None
            
    def convert_VOC_CLASSID_to_CLASSID(self, _id):
        #NOTE: VOC stand for VOC video dataset. 
        #These ID is output buy SSD model (for now, since SSD is trained on VOC)
        #TODO: convert VOC ID into our customed Class ID
        #example: 6 --> 1 (BUS)
        if namespace.VOC_CLASS_DICT[_id] in namespace.CLASS_LIST:
            return namespace.CLASS_DICT[namespace.VOC_CLASS_DICT[_id]]
        else: 
            return None
    
    def filter_annotation(self, _annotation):
        #we specify a customized list of popular class. 10 class, based on VOC dataset
        #replace raw class in IMAGENET to our customized class id
        result = []
        for token, anno in _annotation:
            temp = []
            for item in anno:
                obj_id = item[1]
                new_obj_id = self.convert_IMAGENET_CLASSID_to_CLASSID(obj_id)
                if new_obj_id == None:
                    continue
                new_item = copy.deepcopy(item)
                new_item[1] = new_obj_id
                temp.append(new_item)
            result.append([token, temp])
        return result

    def convert_annotation(self, _raw_annotation):
        #TODO: convert raw IMAGENET annotation [file_token:annotation-list] 
        #           into customed structure {dir_token:{[file_token:annotation]}}
        #annotation = pickle.load(open(_annotation_file_path))
        annotation = self.filter_annotation(_raw_annotation)
        annotation_dict = {}
        for ftoken, box_list in annotation:
            dtoken = Converter.get_dirtoken_from_filetoken(ftoken)
            if dtoken not in annotation_dict:
                annotation_dict[dtoken] = {}
            annotation_dict[dtoken][ftoken] = box_list
        return annotation, annotation_dict
    
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
                idx_class = self.convert_VOC_CLASSID_to_CLASSID(idx_vocobj)
                if idx_class == None:
                    #print 'FAILED: ', idx_bbox, idx_vocobj
                    continue
                hi, wi, dh, dw = predictions[0, idx_vocobj, idx_bbox, 1:].numpy()
                result.append([0, idx_class, score, hi, wi, dh, dw])

        #final steps: convert VOC id to customized id
        return result
    
    