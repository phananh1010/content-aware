import os
import glob
import pickle
import pandas as pd
import re

import utils
import namespace

class YoutubeBBConverter(object):
    #TODO: given raw videos and directory structure, 
    #input: csv files with info tuple (vid, time, cid, oid, bbox)
    #output: {vid+cid+oid: {[]}}
    
    
    
    def __init__(self):
        return

    def remove_refundant_frames(self, vid_dirpath):
        #TODO: remove frames not annotated (in .csv files). 
        #        check if frame idx is divisible to 30 or not. If not, remove
        #INPUT: dir path to the folder containing the videos
        #       #vidpath = namespace.DIRPATH_YOUTUBE_VIDEOS
        #OUTPUT: removed frames from specified folders
        
        for vidpath in glob.glob(vid_dirpath + '/*/*'):
            for img_idx, imgpath in enumerate(glob.glob(vidpath + '/*.jpg')): 
                if img_idx % 30 == 0:
                    imgdirpath, imgname = os.path.dirname(imgpath), os.path.basename(imgpath)
                    imgname = namespace.FILETEMPLATE_FRAMEID.format(img_idx/30) + '.jpg'
                    new_imgpath = imgdirpath + '/' + imgname
                    print 'mv {} {}'.format(imgpath, new_imgpath)
                    os.system('mv {} {}'.format(imgpath, new_imgpath))
            print 'removing {}'.format(vidpath + '/temp*.jpg')
            os.system('rm {}'.format(vidpath + '/temp*.jpg'))
    
    def create_frame_from_vid(self, vid_dirpath):
        #TODO: execute bash script, split videos into frame
        #INPUT: vid_dirpath is folder contains all youtube videos
        #OUPUT: frames in respetive directory, no direct return values
        
        #NOTE: for faster debugging, use this command to remove .jpg file: 
        #          find . -name \*.jpg -type f -delete

        #vidpath = namespace.DIRPATH_YOUTUBE_VIDEOS

        cmd_split_template = 'ffmpeg -i {} {}/temp%06d.jpg -hide_banner'
        cmd_rm_template = ''
        
        #go through all mp4 videos in the folder specified by vid_dirpath
        #split the videos, put frames in to folder has same name as the video
        
        for vidpath in glob.glob(vid_dirpath + '/*/*.mp4'):   
            dirpath = vidpath.replace('.mp4', '')
            print 'creating directory: {}'.format(dirpath)
            os.system('mkdir {}'.format(dirpath))
            print 'split videos into frame into directory above'
            cmd_split = cmd_split_template.format(vidpath, dirpath)
            os.system(cmd_split)
        self.remove_refundant_frames(vid_dirpath)
    
    def process_annotated_item(self, df, vid, cid0, oid):
        #TODO: find minimal time for the video segment, which uniquely defined by vid, cid, oid
        #INPUT: dataframe of whole annotation, (vid, cid, oid) tuple
        #OUTPUT: one annotated item for the video segment.
        #        format: {tfoken:[[0.0, cid, 1.0, xmin, ymin, xmax, ymax]]}

        #step 1, filter dataframe based on (vid, cid0, oid)
        cid_pos = 1  #header index of cid
        oid_pos = 3  #header index of oid
        t_pos = 0
        df_vid = df.loc[vid]
        df_vid = df_vid[(df_vid.iloc[:, cid_pos]==cid0) & (df_vid.iloc[:, oid_pos]==oid)]

        #step 2, iter row, add annotated item
        yanno_val = {}
        
        t_offset = df_vid.iloc[:, t_pos].min()
        for row in df_vid.iterrows():
            r_vid, (r_t, r_cid0, r_cname, r_oid, r_present, r_xmin, r_xmax, r_ymin, r_ymax) = row
            r_cid = utils.convert_YOUTUBE_CLASSID_to_CLASSID(r_cid0)

            #if r_cid != cid or vid != r_vid or oid != r_oid:
            #    raise Exception  #safety measure

            dtoken = utils.create_dtoken(r_vid, r_cid, r_oid)
            ftoken = utils.create_ftoken(dtoken, (r_t-t_offset)/1000)

            #item = (ftoken, (0.0, cid, 1.0, xmin, xmax, ymin, ymax))
            if ftoken not in yanno_val:
                yanno_val[ftoken] = []
            yanno_val[ftoken].append((0.0, r_cid, 1.0, r_xmin, r_ymin, r_xmax, r_ymax))
        return dtoken, yanno_val
    
    def parse_annotation(self, filepath_csv_anno, filepath_out):
        #NOTE: only did once, the second time, should load it
        #TODO: sparse the raw csv annotation provided by YoutubeBB dataset
        #INPUT: file path to the raw csv. 
        #        Could be found here: https://research.google.com/youtube-bb/
        #OUTPUT: yanno, a list of annotation item. yanno_dict, a dict of annotation, keyed by vid+cid+oid
        #TESTDATA: from './data/YOUTUBE_data/yt_bb_detection_train.csv'
        #            write to './data/YOUTUBE_data/yanno_dict'
        
        processed_vidsegment_list = set()
        df = pd.read_pickle(filepath_csv_anno, compression='gzip')
        
        yanno, yanno_dict = [], {}
        
        for row in df.iterrows():
            #we process by agreegate all annotation for a segment, which uniquely defined by (vid, cid0, and oid)
            #if a row is either:
            #       + cnd1: has (vid, cid0, oid) been processed
            #       + cnd2: has unsupported cid
            #then skip the row.
            #else:
            #filter all rows in df has same (vid, cid, and oid)  
            
            vid, (t, cid0, cname, oid, present, xmin, xmax, ymin, ymax) = row
            cid = utils.convert_YOUTUBE_CLASSID_to_CLASSID(cid0)

            #cnd1
            if (vid, cid0, oid) in processed_vidsegment_list:
                continue
                
            #cnd2
            if cid == None:
                continue
            
            processed_vidsegment_list.add((vid, cid0, oid))
            
            dtoken, yanno_item = self.process_annotated_item(df, vid, cid0, oid)
            yanno_dict[dtoken] = yanno_item
            yanno += yanno_item.values()
        
        pickle.dump((yanno, yanno_dict), open(filepath_out, 'w'))

    
    def load_annotation(self, filepath):
        yanno, yanno_dict = pickle.load(open(filepath))
        return yanno, yanno_dict
    
    
    