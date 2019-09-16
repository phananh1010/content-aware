#TODO: filter out frames based on the fps, use python code to do it
#INPUT viddir_wildcard, list of videos to be remove redundant
#OUTPUT: images in each bitrate&resolution directories are trimmed

#HOW: iterate over video names
#template: /home/u9167/content_aware/data/YOUTUBE_data/videos/*/*.mp4
#for each video, iterate over resolution level and bitrate level, go into the folder
#/home/u9167/content_aware/data/YOUTUBE_data/videos/0/{vid}/frames_x{}_b{}
#/home/u9167/content_aware/data/YOUTUBE_data/videos/0/95Gh1o1M94s+0+1/frames_x720_b1024k

import youtubebb_converter
import log_parser
import namespace

LogParser = log_parser.LogParser()
#ONLY run once
#LogParser.runsh_get_videometainfo(namespace.FILEPATH_SCRIPTS_GETINFO, namespace.DIRPATH_YOUTUBE_VIDEOS, namespace.FILEPATH_YOUTUBE_VID_METAINFO)

_, vidinfo_dict, _ = LogParser.parse_video_metainfo(namespace.FILEPATH_YOUTUBE_VID_METAINFO)
YConverter = youtubebb_converter.YoutubeBBConverter(vidinfo_dict)
vid_wildcard = namespace.DIRPATH_YOUTUBE_VIDEOS + '/' + '*/*.mp4'
YConverter.remove_refundant_frames(vid_wildcard)