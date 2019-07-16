#!/bin/bash
#STEP 2 in the SPLIT FEATURE
#TODO from video GOP segment, convert into different bitrate version.
#INPUT: ${1} is a wildcard match all ixxx.mp4 file (GOP segmented in STEP1)
#OUTPUT: videos in different bitrate & resolution, put into same folder with files in ${1}

#USAGE: ./split2_scale_segment.sh /home/u9167/content_aware/data/YOUTUBE_data/videos/\*/\*/i\?\?\?.mp4
#   to remove the result, use this: 
#       find /home/u9167/content_aware/data/YOUTUBE_data/videos/ -name \*x\*b\*.mp4 -type f -delete

HOME=~/content_aware
DIR_YOUTUBE_VIDEO=${HOME}/data/YOUTUBE_data/videos
DIR_SCRIPT=${HOME}/scripts

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
                 
declare -a arr_brm=(2252k 1126k 563k 281k 140k 70k 40k
                   2252k 1126k 563k 281k 140k 70k 40k
                         1126k 563k 281k 140k 70k 40k
                               563k 281k 140k 70k 40k
                                    281k 140k 70k 40k
                                         140k 70k 40k
                 )                 
                 
declare -a arr_bf=(1024k 512k 256k 128k 64k 16k 8k
                   1024k 512k 256k 128k 64k 16k 8k
                         512k 256k 128k 64k 16k 8k
                              256k 128k 64k 16k 8k
                                   128k 64k 16k 8k
                                        64k 16k 8k
                 )                 
                                    

cd $DIR_YOUTUBE_VIDEO
#go through GOP segmented videos 
#for filepath in ${DIR_YOUTUBE_VIDEO}/*/*/i???.mp4
for filepath in ${1}
do
    [ -e "$filepath" ] || continue
    echo "Converting this SOP segmented vid into bitrate & resolution: "
    echo $filepath
    
    N=${#arr_rs[@]}
    for ((i=0;i<$N;i++))
    do
       rs=${arr_rs[$i]}
       brm=${arr_brm[$i]}
       br=${arr_br[$i]}
       bf=${arr_bf[$i]}
       out_filepath=${filepath/.mp4/_x${rs}_b${br}.mp4}
       echo "CMD: ffmpeg -i $filepath -vf scale=-2:${rs} -maxrate ${brm} -bufsize ${bf} ${out_filepath}"
       ffmpeg -i $filepath -vf scale=-2:${rs} -maxrate ${brm} -bufsize ${bf} ${out_filepath}
    done
done