import numpy as np
import re
import os
import namespace

def slice_array(x, pos_begin, pos_end):
    #TODO: get a slice of 1D array. If the begin & end position is out of the array, round it to the array boundary 
    if pos_begin < 0:
        pos_begin = 0
    if pos_end < 0:
        pos_end = len(x)
    return x[pos_begin:pos_end+1]

def moving_average(x, step=10):
    #smooth the array using moving average algorithm
    result = []
    for idx,_ in enumerate(x):
        #print idx-step/2,idx+step/2
        result.append(np.mean(slice_array(x,idx-step,idx+step)))
    return result


def convert_YOUTUBE_CLASSID_to_CLASSID(_id):
        #TODO: convert YoutubeBB ID into our customed Class ID
        #example: 0 (person) --> 11 (person)
        if namespace.YOUTUBE_CLASS_DICT[_id] in namespace.CLASS_LIST:
            return namespace.CLASS_DICT[namespace.YOUTUBE_CLASS_DICT[_id]]
        else: 
            return None
        
        
def convert_IMAGENET_CLASSID_to_CLASSID(_id):
        #NOTE: VID stand for IMAGE VID dataset
        #TODO: convert ImageNet ID into our customed Class ID
        #example: 'n02691156' --> 1
        if namespace.VID_CLASS_DICT[_id] in namespace.CLASS_LIST:
            return namespace.CLASS_DICT[namespace.VID_CLASS_DICT[_id]]
        else: 
            return None
        
def convert_VOC_CLASSID_to_CLASSID(_id):
        #NOTE: VOC stand for VOC video dataset. 
        #These ID is output buy SSD model (for now, since SSD is trained on VOC)
        #TODO: convert VOC ID into our customed Class ID
        #example: 6 --> 1 (BUS)
        if namespace.VOC_CLASS_DICT[_id] in namespace.CLASS_LIST:
            return namespace.CLASS_DICT[namespace.VOC_CLASS_DICT[_id]]
        else: 
            return None

def parse_vidpath(_vidpath):
        #TODO: decompose video path into video name, cid, oid
        vidname, cid0, oid = re.split('\.|/|\+', _vidpath)[-4:-1]
        return vidname, int(cid0), int(oid)
        
def get_dirtoken_from_vidpath(_vidpath):
        #TODO: get dtoken from video filename
        vidname, cid0, oid = parse_vidpath(_vidpath)
        cid = str(convert_YOUTUBE_CLASSID_to_CLASSID(int(cid0)))
        return '+'.join([vidname, str(cid), str(oid)])
    

def get_vidpath_from_dirpath(_dirpath):
        return _dirpath + '.mp4'
    

def get_filetoken_from_imgpath(_imgpath):
        base_path, ext = os.path.splitext(_imgpath) #base_path is filepath with no file extension
        base_imgname = os.path.basename(base_path)  #imgname with no .jpg extention
        dirpath = os.path.dirname(base_path)   #path to parent directory
        vidpath = get_vidpath_from_dirpath(dirpath)
        dtoken = get_dirtoken_from_vidpath(vidpath)
        ftoken = create_ftoken(dtoken, base_imgname)#note: base_imgname is a number
        
        return ftoken
    
def get_vidpath_from_imgpath(_imgpath):
    dirpath = os.path.dirname(_imgpath)
    return get_vidpath_from_dirpath(dirpath)

def get_dirtoken_from_imgpath(_imgpath):
    vidpath = get_vidpath_from_imgpath(_imgpath)
    dtoken = get_dirtoken_from_vidpath(vidpath)
    return dtoken
        
def create_dtoken(vid, cid, oid):
        #TODO: create a dir token, uniquely define a video segment. 
        #INPUT: video name (vid), class id (cid), object id (oid). 
        #        Those values are provided inside the .csv file from YoutubeBB dataset. 
        #         note, cid is our own customed code, not the one in .csv file
        #OUTPUT: the dir token, format vid+cid+oid
        
        cid = int(cid)
        oid = int(oid)
        return '{}+{}+{}'.format(vid, cid, oid)
    
def create_ftoken(dtoken, idx):
        #TODO: create file token, uniquely define a frame
        #      the video is plitted into frames in 1 second intervals. 
        #         Use timestamp column for this information
        #INPUT: dir-token from above function, timestamp related to the annotation
        #OUTPUT: file-token, format dirtoken+timestamp
        return '{}+{}'.format(dtoken, int(idx))     