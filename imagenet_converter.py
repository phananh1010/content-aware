from xml.etree import ElementTree as ET
import namespace
import copy
import re

class ImageNetConverter(object):
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
        #input: a token for a frame or a file, input MUST be an filetoken 
        #output: a token for a video or a directory containing those input frame
        #example input: ILSVRC2015_VID_train_0000_ILSVRC2015_train_00119016_000009
        #example output: ILSVRC2015_VID_train_0000_ILSVRC2015_train_00119016
        return '_'.join(_file_token.split('_')[:-1])
    
    #First functionality, convert raw imagenet ground truth annotation to customed
    

    def convert_IMAGENET_xmlanno_to(_xml_path):
        #TODO: convert IMAGENET xml annotation to the list of standard annotation 
        #          [[0.0, class_idx, confidence, hi, wi, dh, hw]]
        #INPUT: FILE PATH TO THE XML GROUND TRUTH
        #OUTPUT: groundtruth list of item: 0, class
        tree = ET.parse(_xml_path)
        root = tree.getroot()
        w, h = map(float, (root.find('size').find('width').text, root.find('size').find('height').text))

        result = []
        for obj in root.iter('object'):
            obj_id = int(obj.find('trackid').text)
            class_id = obj.find('name').text
            xmax = float(obj.find('bndbox').find('xmax').text)
            xmin = float(obj.find('bndbox').find('xmin').text)
            ymax = float(obj.find('bndbox').find('ymax').text)
            ymin = float(obj.find('bndbox').find('ymin').text)

            result.append([0.0, class_id, 1.0, xmin/w, ymin/h, xmax/w, ymax/h])
        return result
            
    
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
    

    
    