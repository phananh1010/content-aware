import log_parser_namespace
import pickle
import sys
import os
import numpy as np

import __future__

#NOTE: this module expect result from scripts/segmentinfo/metainfo_<ID>.txt'
#      these log file are created from getmeta1_extractinfo.sh
#      this scripts need split0_get_vidlist.sh; split1_get_segment.sh; split2_scale_segment.sh to be executed
#

class LogParser(object):
    _VID_METAINFO_DICT_FILEPATH = '_vid_metainfo_dict'
    def __init__(self):
        #try to open specified file, if not exist, then create such file
        try:
            tmp = pickle.load(open(self._VID_METAINFO_DICT_FILEPATH))
        except Exception as inst:
            print (type(inst), inst.args)#, inst))
            print ('Continue..., will create empty metainfo_dict file')
            pickle.dump({}, open(self._VID_METAINFO_DICT_FILEPATH, 'w'))
        return
    
    def load_metainfo_dict(self):
        vid_metainfo = pickle.load(open(self._VID_METAINFO_DICT_FILEPATH))
        return vid_metainfo
    
    def parse_item(self, item):
        #TODO: given a block of logfile, create an array contain the information of the video segment
        #INPUT: an block of the logfile, see example belows
        #OUTPUT: an array (height, weight, fps, actual_bitrate)
        #sample data:
        #['/home/u9167/content_aware/data/YOUTUBE_data/videos/15/WybwAHSpQdY+15+0/i002_x144_b32k.mp4',
        #   'width=256', 'height=144', 'r_frame_rate=30000/1001',
        #   'duration=1.335000', 'bit_rate=45302']
        k = item[0]
        w = item[1]
        h = item[2]
        fps = item[3]
        duration = item[4]
        b = item[5]
        
        dir_list = os.path.splitext(k)[0].split('/')     #expected a list of parent dirs from filepath
        k1, k2 = dir_list[-2], dir_list[-1]
        w = int(w.split('=')[-1])
        h = int(h.split('=')[-1])
        b = float(b.split('=')[-1])
        duration = float(duration.split('=')[-1])
        #fps = float(eval(fps.split('=')[-1]))
        fps = eval(compile(fps.split('=')[-1], '<string>', 'eval', __future__.division.compiler_flag))

        return (k1, k2), (h, w, fps, b, duration)
    
    def parse_video_metainfo(self, ID):
        #TODO: parse filepath_log into dict structure, add the info into metainfo_dict
        #INPUT: ID of the class to be parsed
        #OUTPUT: updated vid_metainfo_dict
        
        #load the dictionary from file
        vid_metainfo = self.load_metainfo_dict()
        
        filepath_log = log_parser_namespace.LOG_FILETEMPLATE.format(ID)
        dat_raw = np.array(open(filepath_log).read().split('\n')[:-1])
        
        try:
            dat_raw = dat_raw.reshape(-1, log_parser_namespace.BLOCK_SIZE)
        except Exception as inst:
            #throw a notice that segmenting & collecting info has not been finished yet
            print (type(inst), inst.args)#, inst)
            print ('ID={} is not finished'.format(ID))
            
            #now continue
            dat_raw = dat_raw[:len(dat_raw)-len(dat_raw)%log_parser_namespace.BLOCK_SIZE]
            dat_raw = dat_raw.reshape(-1, log_parser_namespace.BLOCK_SIZE)
        
        for item in dat_raw:
            (k1, k2), v = self.parse_item(item)
            if k1 not in vid_metainfo:
                vid_metainfo[k1] = {}
            vid_metainfo[k1][k2] = v
        
        #write back the dictionary to file
        pickle.dump(vid_metainfo, open(self._VID_METAINFO_DICT_FILEPATH, 'w'))
        return vid_metainfo
    
    #OLD CODE, NEED CHANGE
    def parse_video_metainfov0(self, filepath_log):
        #TODO: assuming get_info.sh returned a log file containing metadata of IMAGENET VID videos
        #        now parse the log file to store the metainfo in a dict structure
        #INPUT: filepath for log file containing metadata of videos
        #OUTPUT: result_dict & result_list are a dictionary and a list containing video_filename
        #       w_list, b_list & f_list are list of  (h, w), bitrate (Mbps), and filename
        
        #NOTE!!: this file only parse the raw videos, which is insufficient. Must change this to parse
        #the file named 
        
        raw_dat = open(filepath_log).read().split('\n')
        result_dict = {}
        result_list = []
        w_list = []
        b_list = []
        f_list = []
        
        RECORD_SIZE = 9
        
        for i in range(len(raw_dat)/RECORD_SIZE):
            k = raw_dat[i*RECORD_SIZE]
            w = raw_dat[i*RECORD_SIZE+1]
            h = raw_dat[i*RECORD_SIZE+2]
            fps = raw_dat[i*RECORD_SIZE+3]
            duration = raw_dat[i*RECORD_SIZE+4]
            b = raw_dat[i*RECORD_SIZE+5]

            f = os.path.split(os.path.splitext(k)[0])[1]#what is this command?
            w = int(w.split('=')[-1])
            h = int(h.split('=')[-1])
            b = float(b.split('=')[-1])*1e-6
            #fps = float(eval(fps.split('=')[-1]))
            fps = eval(compile(fps.split('=')[-1], '<string>', 'eval', __future__.division.compiler_flag))

            result_dict[f] = ((h, w, fps, b))
            result_list.append((f, h, w, fps, b))
            w_list.append((h, w))
            b_list.append(b)
            f_list.append(f)
        
        return result_list, result_dict, (f_list, b_list, w_list)
    
    
    #OBSOLETE, SHOULD NOT BE USED
    def runsh_get_videometainfo(self, filepath_script, dirpath_youtube_videos, filepath_vidmetainfo):
        vid_wildcard = dirpath_youtube_videos + '/\*/\*.mp4' #raw videos
        cmd_str = '{} {} {}'.format(filepath_script, vid_wildcard, filepath_vidmetainfo)
        print ("EXECUTING CMD: {}".format(cmd_str))
        os.system(cmd_str)
        return