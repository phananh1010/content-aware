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
To utilize IntelDevcloud, use qsub scripts. The name of the qsub file is `qsub_run_get_youtube_vidlist`.
Inside the `qsub_run_get_youtube_vidlist` file, manually change the number to specify the video category. The qsub script will look into filelist folder, read all video files, and execute all `main sh` scripts.

## Step-by-step
1) Step0 create a video filepath list inside scripts/filelist/ folder
```./split0_get_vidlist.sh ${ID}```

2) Step1 separate video into GOP segments, and 
```./split1_get_segment.sh ${ID}```

3) Step2 create different bitrate, resolution versions for each GOP
```./split2_scale_segment.sh ${ID}```

From step0 to step 2 can be done by running following script in side ./scripts folder:
```qsub -v ID=${ID} qsub_split2_scale_segment```

4) Use ffmpeg to collect video information such as filepath, bitrate, solution, duration, fps. 
Put into segmentinfo/ folders for each CAT ID
5) Use Python to parse the collected segment video information in step (4), put into Python dict
```
import log_parser
Parser = log_parser.LogParser()
for ID in [0, 1, 10, 15, 19, 21 ,23, 4, 7]:
    try:
        Parser.parse_video_metainfo(ID)
    except Exception, e:
        print (e, 'SKIPPED ID={}'.format(ID))
        continue
```
6) Split the segment into frames
```./split3_split_segment.sh ${ID}```

To utilize the batch mode in Intel Devcloud, use qsub:
```qsub -v ID=${ID} qsub_split3_split_segment```

7) Filter out irrelevant frames
Use python code in `split4_filter_frame.py` to filter out irrelevant/non annotated frames
Note: the input is a mask reflect the original videos to be process. The example below is the wild card to all videos belong to CAT 15 (train):
```/home/u9167/content_aware/data/YOUTUBE_data/videos/15/*.mp4``` #3zcr2YpUk1M+15+0

7) (B) Manually remove irrelevant frames (this additional step is needed)
Type following command to remove redundant frames, which previous step 7 missed
```ls /home/u9167/content_aware/data/YOUTUBE_data/videos/<ID>/*/*/????????.jpg```
The command remove all .jpg files has length of 8

After filtering, it is necessary to verify if the filtered frames actually match the annotation from Youtube-BB. Following step by step python instruction in `USAGE_verify_split3_frame_filtering.ipynb` file to retrive the data and visualize the bounding boxes on extracted/filtered frames

8) Create the groundtruth Python dict. Key is the video and ground truth are mAP for each frames
User either following command since the processing time is quick
```python split5_generate_groundtruth.py 19```
or
```qsub qsub_split5_get_groundtruth```



## Other misc
### Target dataset:
We are using the YOUTUBE dataset, which can be downloaded from [YouTube-BB](https://research.google.com/youtube-bb/) website. To extract only annotated video segments, we needed to expande this tool. Note: this tool use youtube-dl to download videos, however, it needs some modification to download the highest resolution. (Currently download 720p by default.)

### Extract list of 1080p video
Use `get_youtube_1080x_videolist.py`

To utilize Intel DevCloud, use qsub script provided in `qsub_run_get_youtube_vidlist`

