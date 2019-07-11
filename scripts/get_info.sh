#!/bin/bash
#TODO: get video meta info for all videos
#INPUT: $1 provides path to the folder containg the videos. 
#         Example input: ./data/YOUTUBE_data/videos/
#        $2 provides path to the file containing the result
#OUTPUT: file vid_metainfo.txt
echo "provided path is ${1}"
echo "current folder is: $(pwd)"
echo "$(ls ${1})"
for filename in ${1}/*/*.mp4; do
    [ -e "$filename" ] || continue
    # ... rest of the loop body
    #echo $filename >> ../data/VID_data/log_scaledvid_metainfo.txt  
    echo $filename >> ${2}
    
    #ffprobe -v error -select_streams v:0 -show_entries stream=width,height $filename >> log.txt
    #ffprobe -v error -show_entries stream=width,height,bit_rate,duration -of default=noprint_wrappers=1 $filename >> vid_metainfo.txt
    ffprobe -v error -show_entries stream=width,height,bit_rate,duration,r_frame_rate -of default=noprint_wrappers=1 $filename >> ${2}
done
