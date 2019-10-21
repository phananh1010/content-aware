import pandas as pd
import cv2
import numpy as np
import glob
import os
import pickle
import sys

import namespace
import log_parser
import youtubebb_converter
import imagenet_converter
import dataset_generator
import metric_map
import predictor
import utils
def get_groundtruth_item(img_filepath, vid_filepath, pred):
    #TODO: 
    img = cv2.imread(img_filepath, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    dtoken, ftoken = utils.get_dirtoken_from_vidpath(vid_filepath), utils.get_filetoken_from_imgpath(vid_filepath, img_filepath)
    gt_list = yanno_dict[dtoken][ftoken]
    
    pred_list = pred.detect(img)
    if pred_list == []:
        #print ('DETECTED NOTHING for {}, SKIPPED'.format(img_filepath))
        return 0.0#gt_list[0], pred_list, 0.0
    #plot_bbox(rgb_img, pred_list[0])
    #plot_bbox(rgb_img, gt_list[0], color_idx=10)

    score = mAP.score(pred_list, gt_list)
    return score#gt_list[0], pred_list, score

def get_all_frameversions(frame_filepath, vid_filepath, pred):
    #TODO: for a given frame in max bitrate & max resolution (x1080_b1024), 
    #retrive corresponding frames in other bitrates & resolutions
    #INPUT: a filepath to frame in highest res & bit
    #OUTPUT: grouthtruth for everyone
    
    frame_filemask = frame_filepath.replace(namespace.FRAMEVERSION_BEST, '*')
    result = []
    for img_filepath in glob.glob(frame_filemask):
        result.append(get_groundtruth_item(img_filepath, vid_filepath, pred))
    return result

def generate_viditem_groundtruth(vidpath, pred):
    #TODO: generate ground truth from given video path
    #INPUT: path to video, predictor
    #OUTPUT: dict structure store groundtruth all frames for that video
    result = {}
    framemask = os.path.splitext(vidpath)[0] + '/' + namespace.FRAMEVERSION_BEST + '/??????.jpg'
    for framepath in glob.glob(framemask): #go over all frame item in the best verion
        #for each best frame item, collect score over all of its versions
        #print item
        try:
            gt_list = get_all_frameversions(framepath, vidpath, pred)
        except:
            print 'ERROR: ', framepath, vidpath
            raise
        result[framepath] = gt_list
    return vidpath, result

#in order for log_parser to work, previous steps are assumed to be taken.
#see https://github.com/phananh1010/content-aware/tree/master/scripts for further detail

LogParser = log_parser.LogParser()
vidinfo_dict= LogParser.load_metainfo_dict()

YConverter = youtubebb_converter.YoutubeBBConverter(vidinfo_dict)
mAP = metric_map.mAP()
Pred  = predictor.Predictor()

#only run once to create processed Youtube annotation dict, write to FILEPATH_YOUTUBE_YANNODICT
#YConverter.parse_annotation(namespace.FILEPATH_YOUTUBE_RAWANNOCSV, namespace.FILEPATH_YOUTUBE_YANNODICT)
yanno, yanno_dict = YConverter.load_annotation(namespace.FILEPATH_YOUTUBE_YANNODICT)
DatGen = dataset_generator.DatasetGenerator(YConverter, mAP, Pred, yanno_dict)

#for debuging purpose only
df = pd.DataFrame.from_csv('./data/YOUTUBE_data/yt_bb_detection_train.csv', header=None)
df1 = pd.read_pickle('./data/YOUTUBE_data/yt_bb_detection_train_filtered.pkl.gz', compression='gzip')
                            #./data/YOUTUBE_data/yt_bb_detection_train_filtered.csv

ID = sys.argv[1]
    
_GROUNDTRUTH_DICT_TEMPLATE_ = namespace.GROUNDTRUTH_DICT_TEMPLATE
GROUNDTRUTH_DICT_FILEPATH = _GROUNDTRUTH_DICT_TEMPLATE_.format(ID)
vidmask = namespace.DIRPATH_YOUTUBE_VIDEOS + '/{}/'.format(ID) + '*.mp4'

gt_dict = {}
try:
    gt_dict = pickle.load(open(GROUNDTRUTH_DICT_FILEPATH))
except:
    print 'ERROR, no file found, will use default empty dic'
    

for vid_filepath in glob.glob(vidmask):
    if vid_filepath in gt_dict: 
        print ("SKIPPED {}".format(vid_filepath))
        continue
    print ('processing {}'.format(vid_filepath))
    try:
        k, v = generate_viditem_groundtruth(vid_filepath, Pred)
        gt_dict[k] = v
        pickle.dump(gt_dict, open(GROUNDTRUTH_DICT_FILEPATH, 'w'))
    except: 
        print ("SKIPPED {} EXCEPTION".format(vid_filepath))
        continue