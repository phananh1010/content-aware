This is the instruction on how to use our scripts to split the videos into frames at different bitrate & resolution.

## Overview
There are four main steps:
### Step 0: download original youtube videos
`Main sh` file: `split0_get_vidlist.sh`
Refer to the Tower machine for downloaded vid, put to Intel Devcloud in this path:
`.../content_aware/data/YOUTUBE_data/videos_bk/videos_bk/videos/yt_bb_detection_train/<CAT>/<vid_name>.mp4`
Then run `split0_get_vidlist.sh` to put video filepaths into files inside `filelist` folder

### Step 1: split videos into GOP segment, this is necessary since each segment has different bitrates. From now on, the bitrate of any frames is the bitrate of the GOP segment in which it belongs to.
`Main sh` file: `split1_get_segment.sh`
### Step 2: for each raw GOP segment, split into different bitrates & resolution levels.
`Main sh` file: `split2_scale_segment.sh`
### Step 3: for each transformed GOP segment, extract to individual frames.
`Main sh` file: `split3_split_segment.sh`
### Step 4: each extracted frame is input to `YOLO`/`SSD` model. Here the Object Detection results scored in mAP are recorded
`Main sh` file: `split4_filter_frame.py`

## Description
### Main sh files:
INPUT: all main sh file receive a list of videos to be executed. 
OUTPUT: the output are invidual .mp4 or frames, put into correponding folders in the following path
```.../content_aware/data/YOUTUBE_data/videos```


### `filelist` folder: 
to create such filelist, execute this command:
```for f in /home/u9167/content_aware/data/YOUTUBE_data/videos/7/*.mp4; do printf "${f}\n" >> filelist/7.txt; done```

### run batch job using `qsub`
To utilize IntelDevcloud, use qsub scripts. The name of the qsub file is `qsub_run_get_youtube_vidlist`
Inside the `qsub_run_get_youtube_vidlist` file, manually change the number to specify the video category. The qsub script will look into filelist folder, read all video files, and execute all `main sh` scripts.

## Other misc

### target dataset:
We are using the YOUTUBE dataset, which can be downloaded from [YouTube-BB](https://research.google.com/youtube-bb/) website. To extract only annotated video segments, we needed to expande this tool. Note: this tool use youtube-dl to download videos, however, it needs some modification to download the highest resolution. (Currently download 720p by default.)

### extract list of 1080p video
Using `get_youtube_1080x_videolist.py`
To utilize Intel DevCloud, use qsub script provided in `qsub_run_get_youtube_vidlist`

