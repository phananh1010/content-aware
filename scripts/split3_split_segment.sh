#!/bin/bash
#TODO: for the given video in different bitrate&resolution, now split the video into INDIVIDUAL frames. 
#   Step 1: create a filders for each bitrate & resolution level
#   step 2: split the videos into frames
#INPUT: path to original mp4 videos
#     the algorithm will point to the directory where file has been segmented and convert to different bitrates, resolution
#OUTPUT: folders contain individual frames

#USAGE: ./split3_split_segment.sh /home/u9167/content_aware/data/YOUTUBE_data/videos/\*/\*.mp4

#WARNING: this script generate ALL frame based on fps information.
#need to run python code to filter out annotated frame
declare -a arr_rs=(1080 1080 1080 1080 1080 1080 1080
                       720 720 720 720 720 720 720
                          480 480 480 480 480 480
                              360 360 360 360 360
                                  240 240 240 240
                                      144 144 144
                   )
declare -a arr_br=(2048k 1024k 512k 256k 128k 64k 32k
                   2048k 1024k 512k 256k 128k 64k 32k
                       1024k 512k 256k 128k 64k 32k
                            512k 256k 128k 64k 32k
                                256k 128k 64k 32k
                                    128k 64k 32k
                   )
                                    
echo ${1}
for filepath in ${1}; do
    [ -e "$filepath" ] || continue
    echo "splitting to frames for: $filepath"
    
    #NOTE: dirpath points to the dire same name with video file, NOT the parent directory
    dirpath=$(echo "$filepath" | cut -f 1 -d '.')
    
    N=${#arr_rs[@]}
    for ((i=0;i<$N;i++))
    do
       rs=${arr_rs[$i]}
       br=${arr_br[$i]}

       infile_wildcard=${dirpath}/i???_x${rs}_b${br}.mp4
       out_dir=${dirpath}/frames_x${rs}_b${br}
       
       #first, make the directory to contain the frame
       mkdir ${out_dir}
       
       idx=0
       echo '---------'
       #now, iterate over list of video to be splited
       for invidseg in ${infile_wildcard}; do
           [ -e "$invidseg" ] || continue
           echo "CMD: ffmpeg -i $invidseg ${out_dir}/${idx}%06d.jpg -hide_banner"
           ffmpeg -i $invidseg ${out_dir}/${idx}%06d.jpg -hide_banner
           idx=$((idx+1))
       done
       echo '---------'
    done
done