#!/bin/bash
#TODO: get all metainfo about each video segment. print a list of ffmpeg cmd for each segment into an sh file #then execute it

#INPUT: a CAT ID and associated segmentlist, 
#OUTPUT: a metainfo.txt file for all segment of all videos belong to that specific CAT

HOME=/home/u9167/content_aware
DIR_YOUTUBE_VIDEO=${HOME}/data/YOUTUBE_data/videos
DIR_SCRIPTS=${HOME}/scripts
TARGET_CMD_FILE=${DIR_SCRIPTS}/misc/get_metainfo_cmdlist${1}.txt
TARGET_INFO_FILE=${DIR_SCRIPTS}/segmentinfo/metainfo_${1}.txt

rm ${TARGET_CMD_FILE}
rm ${TARGET_INFO_FILE}
while read filepath; do 
    [ -e "$filepath" ] || continue
    #note: each $filepath is an absolute path to a segment of video belong to the ID
    #dirpath=$(echo "$filepath" | cut -f 1 -d '.')
    #echo ${dirpath}
    echo "echo $filepath >> ${TARGET_INFO_FILE}" >> ${TARGET_CMD_FILE}
    echo "ffprobe -v error -show_entries stream=width,height,bit_rate,duration,r_frame_rate -of default=noprint_wrappers=1 $filepath >> ${TARGET_INFO_FILE}" >> ${TARGET_CMD_FILE}
done < ${DIR_SCRIPTS}/segmentlist/${1}.txt
chmod u+x ${TARGET_CMD_FILE}
${TARGET_CMD_FILE}