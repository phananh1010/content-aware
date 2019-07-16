#!/bin/bash
#get all files in raw folder, change its resolution
CURDIR=~/content_aware/scripts
ROOT=~/content_aware/data/YOUTUBE_data
ROOT_RAW=${ROOT}/videos
ROOT_SCALED=${ROOT}/videos_scaled

cd $ROOT
for filepath in ${ROOT_RAW}/*/*.mp4; do
    [ -e "$filepath" ] || continue
    echo "changing resolution to x360, x240, x144 for $filepath"
    #echo "test filename: ${filename/.mp4/_x360.mp4}"
    #algorithm: 
    #  1) create directory named filepath/$filename
    #  2) split the vid into GOP segments
    #  3) change bitrate and resolution for individual segments
    #  4) create directory named ./scaled/$filename/frames
    #  5) split the segments into frames 
    #ffmpeg -i $filename -vf scale=-2:480 ${filename/.mp4/_x480.mp4}
    #ffmpeg -i $filename -vf scale=-1:360 ${filename/.mp4/_x360.mp4}
    #ffmpeg -i $filename -vf scale=-2:240 ${filename/.mp4/_x240.mp4}
    #ffmpeg -i $filename -vf scale=-1:144 ${filename/.mp4/_x144.mp4}
    
    #filename is the file name with .mp4 extension
    filename=$(echo "$filepath" | sed "s/.*\///")
    mkdir ${ROOT_SCALED}/${filename/.mp4/}
    
    #another method. First, create uncompressed video, then measure the bitrate
    ffmpeg -i $filepath -an -c:v copy -segment_time 0.00001 -f segment ${ROOT_SCALED}${filename/.mp4/}/i%0d.mp4
    
    for segname in ${ROOT_SCALED}${filename/.mp4/}/*.mp4; do
        [ -e "$segname" ] || continue
        echo "now processing segment $segname"
        ffmpeg -i $segname -maxrate 2148k -bufsize 1024k ${segname/.mp4/_x720_b2048.mp4}
        ffmpeg -i $segname -maxrate 1124k -bufsize 512k ${segname/.mp4/_x720_b1024.mp4}
        ffmpeg -i $segname -maxrate 522k -bufsize 256k ${segname/.mp4/_x720_b512.mp4}
        ffmpeg -i $segname -maxrate 316k -bufsize 128k ${segname/.mp4/_x720_b256.mp4}
        ffmpeg -i $segname -maxrate 138k -bufsize 64k ${segname/.mp4/_x720_b128.mp4}
        ffmpeg -i $segname -maxrate 68k -bufsize 16k ${segname/.mp4/_x720_b64.mp4}
        ffmpeg -i $segname -maxrate 38k -bufsize 8k ${segname/.mp4/_x720_b32.mp4}
        
        ffmpeg -i $segname -vf scale=-2:480 -maxrate 1124k   -bufsize 512k ${segname/.mp4/_x480_b1024.mp4}
        ffmpeg -i $segname -vf scale=-2:480 -maxrate 522k -bufsize 256k ${segname/.mp4/_x480_b512.mp4}
        ffmpeg -i $segname -vf scale=-2:480 -maxrate 316k -bufsize 128k ${segname/.mp4/_x480_b256.mp4}
        ffmpeg -i $segname -vf scale=-2:480 -maxrate 138k -bufsize 64k ${segname/.mp4/_x480_b128.mp4}
        ffmpeg -i $segname -vf scale=-2:480 -maxrate 68k  -bufsize 16k ${segname/.mp4/_x480_b64.mp4}
        ffmpeg -i $segname -vf scale=-2:480 -maxrate 38k  -bufsize 8k ${segname/.mp4/_x480_b32.mp4}  
        
        ffmpeg -i $segname -vf scale=-1:360 -maxrate 522k -bufsize 256k ${segname/.mp4/_x360_b512.mp4}
        ffmpeg -i $segname -vf scale=-1:360 -maxrate 316k -bufsize 128k ${segname/.mp4/_x360_b256.mp4}
        ffmpeg -i $segname -vf scale=-1:360 -maxrate 138k -bufsize 64k ${segname/.mp4/_x360_b128.mp4}
        ffmpeg -i $segname -vf scale=-1:360 -maxrate 68k -bufsize 16k ${segname/.mp4/_x360_b64.mp4}
        ffmpeg -i $segname -vf scale=-1:360 -maxrate 38k -bufsize 8k ${segname/.mp4/_x360_b32.mp4}
        
        ffmpeg -i $segname -vf scale=-2:240 -maxrate 316k -bufsize 128k ${segname/.mp4/_x240_b256.mp4}
        ffmpeg -i $segname -vf scale=-2:240 -maxrate 138k -bufsize 64k ${segname/.mp4/_x240_b128.mp4}
        ffmpeg -i $segname -vf scale=-2:240 -maxrate 68k -bufsize 16k ${segname/.mp4/_x240_b64.mp4}
        ffmpeg -i $segname -vf scale=-2:240 -maxrate 38k -bufsize 8k ${segname/.mp4/_x240_b32.mp4}
        
        ffmpeg -i $segname -vf scale=-1:144 -maxrate 138k -bufsize 64k ${segname/.mp4/_x144_b128.mp4}
        ffmpeg -i $segname -vf scale=-1:144 -maxrate 68k -bufsize 16k ${segname/.mp4/_x144_b64.mp4}
        ffmpeg -i $segname -vf scale=-1:144 -maxrate 38k -bufsize 8k ${segname/.mp4/_x144_b32.mp4}
        
    done
done
