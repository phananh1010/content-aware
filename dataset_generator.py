
import glob
import pickle
import os
import glob
import cv2 


import utils
import imagenet_converter#need to change to ImagenetConverter
import namespace
import log_parser
import youtubebb_converter

class DatasetGenerator(object):
    #TODO: 
    #1) create mAP lines for each videos. input is image folders, output is mAP lines
    #2) write bash scripts to convert video into different bitrates, resolution, and split them to frames
    #3) 
    def __init__(self, YConverter, mAP, pred_list, yanno_dict):
        #IMAGENET dataset
        #self.anno_dict = anno_dict
        #self.vid_dirtoken_dict = vid_dirtoken_dict
        
        #TODO: provide DatGen with necessary data for initilization
        # .    YConverter need vidinfo_dict, which contains video metadata, to do basic conversion
        #      Pred contain SSD for prediction
        # .    mAP to calculate mAP scores
        #      segpred_dict_filepath is pickle files contain pair of prediction score & ground truth & mAP score for all images
        
        #YOUTUBE dataset
        #commented path is how to generetd required data, in cased of debugging is needed
        #LogParser = log_parser.LogParser()
        #ONLY run once
        #LogParser.runsh_get_videometainfo(namespace.FILEPATH_SCRIPTS_GETINFO, namespace.DIRPATH_YOUTUBE_VIDEOS, namespace.FILEPATH_YOUTUBE_VID_METAINFO)

        #_, vidinfo_dict, _ = LogParser.parse_video_metainfo(namespace.FILEPATH_YOUTUBE_VID_METAINFO)
        #self._YConverter = youtubebb_converter.YoutubeBBConverter(vidinfo_dict)
        #self._mAP = metric_map.mAP()
        #self._Pred  = predictor.Predictor()
        #_, self._yanno_dict = YConverter.load_annotation(namespace.FILEPATH_YOUTUBE_YANNODICT)
        self._YConverter, self._mAP, self._Pred, self._yanno_dict = YConverter, mAP, Pred, yanno_dict
        
        #self._segpred_dict = pickle.load(open(segpred_dict_filepath))
        
        arr_rs = namespace.RESOLUTION_LIST
        arr_br = namespace.BITRATE_LIST
        N      = namespace.NO_RESOLUTION_LEVELS
        self._key_list = [namespace.FILETEMPLATE_FRAMEVERSION.format(arr_rs[idx], arr_br[idx]) for idx in range(N)]
    
    def create_mAP_line(self, dirpath, videoname, mAP, Converter, pred_list, smooth_step=10, to_file=False):
        #TODO: create smoothed mAP lines for IMAGENET dataset, obsolete since now YOUTUBE dataset is used instead
        #INPUT: dirpath contains all video frame for a given video
        #       smooth_step to smooth the mAP results using 10 previous & 10 after frame
        #OUTPUT: generate a smoothed mAP line
        #test sample dirpath: './data/VID_data/ILSVRC2015_VID_train_0000/ILSVRC2015_train_00005004/*'
        filepath_list = glob.glob(dirpath)
        filepath_list = sorted(filepath_list)
        y_raw = []
        
        dtoken = self.vid_dirtoken_dict[videoname]
        for idx, filepath in enumerate(filepath_list):
            if idx%100==0:
                print (idx, filepath)

            ftoken = Converter.get_ftoken_from_vidname_and_idx(self.vid_dirtoken_dict, videoname, idx)
            
            for pred in pred_list:
                y_raw.append(mAP.score_from_file(filepath, Converter, pred, self.anno_dict[dtoken][ftoken]))
                y = utils.moving_average(y_raw)
        
        if to_file == True:
            #ftoken = converter.Converter.get_token_from_filepath(filepath)
            #dtoken = converter.Converter.get_dirtoken_from_filetoken(ftoken)
            pickle.dump(y, open(namespace.DIRPATH_VID_mAP_LINES + namespace.FILETEMPLATE_mAP_LINES.format(dtoken), 'wb'))
            
        return y
    
    
    #from now on, use the following functionalities since we moved to Youtube dataset
    def create_frames_from_vid(self, vidpath_wildcard):
        #TODO: executing ./scripts/split*_ script files to split original videos into annotated frames in different bitrate & resolution versions
        #INPUT: wildcard points to collection of videos to be splitted
        #OUTPUT: the splited frames stored in frames_* folders
        
        #example code:
        #./split1_get_segment.sh  /home/u9167/content_aware/data/YOUTUBE_data/videos/4/akQU-s0RCWE+4+2.mp4
        #./split2_scale_segment.sh /home/u9167/content_aware/data/YOUTUBE_data/videos/4/akQU-s0RCWE+4+2.mp4
        #./split3_split_segment.sh /home/u9167/content_aware/data/YOUTUBE_data/videos/4/akQU-s0RCWE+4+2.mp4
        #execute all Python codes in the split4_filter_frame.py file
        
        cmd_str = '{} {}';
        os.system('cd {}'.format(namespace.DIRPATH_SCRIPTS))
        os.system(cmd_str.format(namespace.FILEPATH_SCRIPTS_SPLIT1, vidpath_wildcard))
        os.system(cmd_str.format(namespace.FILEPATH_SCRIPTS_SPLIT2))
        os.system(cmd_str.format(namespace.FILEPATH_SCRIPTS_SPLIT3))
        os.system('cd {}'.format(namespace.DIRPATH_HOME))
        

        #vid_wildcard = namespace.DIRPATH_YOUTUBE_VIDEOS + '/' + '*/*.mp4'
        self._YConverter.remove_refundant_frames(vidpath_wildcard)
        
    
    def create_segment_predresult_dict(self, segpred_dict_filepath, vid_wildcard):
        #TODO: from video frames in different bitrate&resolution, call the prediction model, get prediction results, calculate mAP scores.
        #INPUT: pickelfilepath to the dict structure hole prediction result and ground truth
        #         vid_wildcard is all videos that need to be updated
        #OUTPUT: the updated dict with entries for new videos, the dict is written to the file
        
        #result = pickle.load(open(namespace.FILEPATH_YOUTUBE_SEGMENT_PREDRESULT))   
        result = pickle.load(open(segpred_dict_filepath))  
        
        #vid_wildcard = namespace.DIRPATH_YOUTUBE_VIDEOS + '/' + '*/*.mp4'
        arr_rs = namespace.RESOLUTION_LIST
        arr_br = namespace.BITRATE_LIST
        N      = namespace.NO_RESOLUTION_LEVELS
        
        for vidpath in glob.glob(vid_wildcard):
            dirpath = os.path.splitext(vidpath)[0]

            if vidpath not in result:
                result[vidpath] = {}
            else:
                continue #we don't redo videos already in the dict

            for idx in range(N):
                rs = arr_rs[idx]
                br = arr_br[idx]
                target_path = dirpath + '/' + 'frames_x{}_b{}'.format(rs, br)

                if target_path not in result[vidpath]:
                    result[vidpath][target_path] = []

                img_wildcard = target_path + '/' + '*.jpg'
                for img_idx, img_path in enumerate(sorted(glob.glob(img_wildcard))):
                    img1 = cv2.imread(img_path, cv2.IMREAD_COLOR)
                    rgb_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

                    pred_list = self._Pred.detect(img1)

                    dtoken, ftoken = utils.get_dirtoken_from_vidpath(vidpath), utils.get_filetoken_from_imgpath(vidpath, img_path)
                    gt_list = self._yanno_dict[dtoken][ftoken]

                    result[vidpath][target_path].append((img_path, gt_list, pred_list, self._mAP.score(pred_list, gt_list)))
    
        #update the dict into file
        pickle.dump(result, open(segpred_dict_filepath, 'w'))   
        
    def get_dat(self, segpred_dict, vid_filepath, img_idx):
        #TODO: create (X, y) for the dataset
        # .    X: load the idx images of the video, 
        # .    y: load the mAP scores from segpred_dict structure
        #INPUT: segpred_dict stores all mAP scores, use `create_segment_predresult_dict` function to create this structure
        # .     vid_filepath point to the video names, which is also the key to access segpred_dict
        #       img_idx is the idx of the image to be retrieved
        #OUTPUT: a pair (X, y)
        
        #example vid_filepath: '/home/u9167/content_aware/data/YOUTUBE_data/videos/0/95Gh1o1M94s+0+1.mp4'
        
        #create X: extract the image
        arr_rs = namespace.RESOLUTION_LIST
        arr_br = namespace.BITRATE_LIST
        N      = namespace.NO_RESOLUTION_LEVELS
        
        version_dir = namespace.FILETEMPLATE_FRAMEVERSION.format(arr_rs[0], arr_br[0])
        img_filename = namespace.FILETEMPLATE_FRAMEID.format(img_idx) + '.jpg'
        image_filepath = vid_filepath.replace('.mp4', '') + '/' + version_dir + '/' + img_filename
        img1 = cv2.imread(image_filepath, cv2.IMREAD_COLOR)
        rgb_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        X = img1
        
        #create y: extract mAP scores from segpred_dict
        y, gt, pred = [], [], []
        for version_pattern in self._key_list:
            version_dir=vid_filepath.replace('.mp4', '') + '/' + version_pattern
            y.append(segpred_dict[vid_filepath][version_dir][img_idx][-1])
            gt.append(segpred_dict[vid_filepath][version_dir][img_idx][1])
            pred.append(segpred_dict[vid_filepath][version_dir][img_idx][2])
        return X, y, gt, pred
            
        
        
      