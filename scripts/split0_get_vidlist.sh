#!/bin/bash
#TODO: retrieve the list of videos which will be used in later steps.
        #Where to look: ...content_aware/data/YOUTUBE_data/videos_bk/videos_bk/videos/yt_bb_detection_train/<id>
#INPUT: a Youtube-BB object class ID from 0-23
#OUTPUT: a list of command on the absolute filepath to be executed
HOME=/home/u9167/content_aware
DIR_SCRIPTS=${HOME}/scripts
DIR_YOUTUBE_VIDEO=${HOME}/data/YOUTUBE_data/videos

find ${DIR_YOUTUBE_VIDEO}/${1}/ -maxdepth 1 -type f -name *.mp4 > ${DIR_SCRIPTS}/filelist/${1}.txt