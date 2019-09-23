#TODO: filter out frames based on the fps, use python code to do it
#INPUT viddir_wildcard, list of videos to be remove redundant
#OUTPUT: images in each bitrate&resolution directories are trimmed



#HOW: iterate over video names
#template: /home/u9167/content_aware/data/YOUTUBE_data/videos/*/*.mp4
#An example of such template:
#/home/u9167/content_aware/data/YOUTUBE_data/videos/15/3zcr2YpUk1M+15+0.mp4
#for each video, iterate over resolution level and bitrate level, go into the folder
#/home/u9167/content_aware/data/YOUTUBE_data/videos/0/{vid}/frames_x{}_b{}
#/home/u9167/content_aware/data/YOUTUBE_data/videos/0//frames_x720_b1024k


import youtubebb_converter
import log_parser
import namespace
import sys

#in order for log_parser to work, previous steps are assumed to be taken.
#see https://github.com/phananh1010/content-aware/tree/master/scripts for further detail
LogParser = log_parser.LogParser()
vidinfo_dict= LogParser.load_metainfo_dict()


YConverter = youtubebb_converter.YoutubeBBConverter(vidinfo_dict)
vid_wildcard = namespace.DIRPATH_YOUTUBE_VIDEOS + '/' + sys.argv[1] + '/*.mp4'#basically, this is the video list
print ('Filtering our irrelevent frames for: ', vid_wildcard)
YConverter.remove_redundant_frames(vid_wildcard)
