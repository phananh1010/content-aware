#!/bin/bash
#TODO: this script split vid segment into frames
#INPUT: receive input from scale_video_resolution_and_bitrate.sh file
#OUTPUT: individual frames from said vid segment. The frame is put into corresponding folders
#ALG: iterate over all vid segment that has the same resolution & bitrate, split into individual frames
#
CURDIR=~/content_aware/scripts/
ROOT=~/content_aware/data/VID_data/
ROOT_RAW=${ROOT}raw/
ROOT_SCALED=${ROOT}scaled/

declare -a arr_vid=("x720_b2048" "x720_b1024" "x720_b512" "x720_b256" "x720_b128" "x720_b64" "x720_b32"
                                 "x480_b1024" "x480_b512" "x480_b256" "x480_b128" "x480_b64" "x480_b32"
                                              "x360_b512" "x360_b256" "x360_b128" "x360_b64" "x360_b32"
                                                          "x240_b256" "x240_b128" "x240_b64" "x240_b32"
                                                                      "x144_b128" "x144_b64" "x144_b32"
                    )

#now, split all video with mask specified by ${arr_vid}
for dirpath in ${ROOT_SCALED}*; do
    [ -e "$dirpath" ] || continue
    for template in "${arr_vid[@]}"; do
        #create directory to hold the frames
        dir_template=${dirpath}/${template};
        echo "creating dir ${dir_template}"
        mkdir ${dir_template}
        
        for filepath in ${dirpath}/*${template}*.mp4; do
            [ -e "$filepath" ] || continue
            #first, create an image template
            filename=$(echo "$filepath" | sed "s/.*\///")
            neg_pattern=_x720_b9999_${template}.mp4
            image_template=${filename/${neg_pattern}/}
            
            #then, split the video
            echo "splitting vid: $filepath into ${dir_template}/${image_template}%04d.jpg"
            ffmpeg -i $filepath ${dir_template}/${image_template}%04d.jpg -hide_banner
        done
    done
done
