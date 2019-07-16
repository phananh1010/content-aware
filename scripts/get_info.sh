#!/bin/bash
#TODO: get video meta info for all videos
#INPUT: $1 provides path to the folder containg the videos. 
#         Example input: ./data/YOUTUBE_data/videos/
#        $2 provides path to the file containing the result
#OUTPUT: file vid_metainfo.txt

#USAGE: to use this file, enter commands similar to this. Pay attention to the * mark
#  ./get_info.sh  /home/u9167/content_aware/data/YOUTUBE_data/videos/\*/\*/\*.mp4 /home/u9167/content_aware/temp/info.txt

echo "provided path is ${1}"
echo "current folder is: $(pwd)"
echo "total params: ${@}"
for filename in ${1}; do
    [ -e "$filename" ] || continue
    # ... rest of the loop body
    #echo $filename >> ../data/VID_data/log_scaledvid_metainfo.txt  
    echo $filename >> ${2}
    
    #ffprobe -v error -select_streams v:0 -show_entries stream=width,height $filename >> log.txt
    #ffprobe -v error -show_entries stream=width,height,bit_rate,duration -of default=noprint_wrappers=1 $filename >> vid_metainfo.txt
    echo "CMD: ffprobe -v error -show_entries stream=width,height,bit_rate,duration,r_frame_rate -of default=noprint_wrappers=1 $filename >> ${2}"
    ffprobe -v error -show_entries stream=width,height,bit_rate,duration,r_frame_rate -of default=noprint_wrappers=1 $filename >> ${2}
done
