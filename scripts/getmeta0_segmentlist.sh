#!/bin/bash
#TODO: get all video segments, FIRST, prepare a list of filepaths corresponse to each segment
#INPUT: a CAT ID and associated filelist, 
HOME=/home/u9167/content_aware
DIR_YOUTUBE_VIDEO=${HOME}/data/YOUTUBE_data/videos
DIR_SCRIPTS=${HOME}/scripts
TARGET_FILE=${DIR_SCRIPTS}/segmentlist/${1}.txt

rm ${TARGET_FILE}
while read filepath; do 
    [ -e "$filepath" ] || continue
    dirpath=$(echo "$filepath" | cut -f 1 -d '.')
    #echo ${dirpath}
    #echo "find ${dirpath}/ -maxdepth 1 -type f -name *.mp4"
    find ${dirpath}/ -maxdepth 1 -type f -name \*x\*b\*.mp4 >> ${TARGET_FILE}
done < ${DIR_SCRIPTS}/filelist/${1}.txt