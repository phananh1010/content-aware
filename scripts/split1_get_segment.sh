#!/bin/bash
#STEP 1 in the SPLIT feature.
#TODO: split the videos into GOP segments to have more accurate information about bitrate.
# .    steps: 
#           - create a folder with the same name as the video
#           - create segments, output into the folder

#USAGE:./split1_get_segment.sh  /home/u9167/content_aware/data/YOUTUBE_data/videos/\*/\*.mp4

HOME=~/content_aware
DIR_YOUTUBE_VIDEO=${HOME}/data/YOUTUBE_data/videos
DIR_SCRIPT=${HOME}/scripts

cd $HOME

#for filepath in ${DIR_YOUTUBE_VIDEO}/*/*.mp4; do
for filepath in ${1}; do
    [ -e "$filepath" ] || continue
    echo "segmenting the $filepath"
    
    #create dirpath same name as video name (without mp4)
    dirpath=$(echo "$filepath" | cut -f 1 -d '.')
    mkdir $dirpath
    
    #then, split the videos into segment, put into the newly created directory
    template_file=${dirpath}/i%03d.mp4
    echo "CMD: ffmpeg -i $filepath -an -c:v copy -segment_time 0.00001 -f segment ${template_file}"
    ffmpeg -i $filepath -an -c:v copy -segment_time 0.00001 -f segment ${template_file}

done
