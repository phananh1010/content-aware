This repository contain source code to train a DCNN to predict the performance of machine learning model.
# content-aware
content-aware-dcnn

NOTE: 
1) download the weights for SSD model [here](https://drive.google.com/file/d/1L7lgaMatPSv-yCMA-Eh_GshJJIaO2vvK/view?usp=sharing) or [here](https://drive.google.com/open?id=1_YhuoPLxQI580J_RiYxcP9lW2kV-pdgf) and put into the ./weights directory
2) download the [imagenet_labels](https://drive.google.com/open?id=1hAf8QraVhOk3IQVQslZ_b1ySU3mJUpu9) and put into root directory. This file contains all annotation data.
3) download the [youtube-bb](https://research.google.com/youtube-bb/) dataset
4) clone the [repository](https://github.com/mbuckler/youtube-bb) to download and segment youtube videos.

General steps
STEP1: process raw youtube vid
from the file yt_bb_detection_train.csv, filter out only videos with 1080x1920p resolutions. Then use the source code at (4) to download and segment the videos.
NOTE: the source code to download & segment youtube-bb dataset has a bug, when the youtube-dl only download 720p videos at max resolution
To fix this issuse, remove best parameter, and adding -c to the end of the script.
Location: inside function dl_and_cut, located in the youtube_bb.py file

STEP2: split the video segment
The videos are localed inside ./data/YOUTUBE_data/videos, store in separated directory. Each directory is named after the class ID. Currently, there are 13 class IDs: 0: PERSON, 1: BIRD, 2: BICYCLE, 3: WATERCRAFT, 4: BUS, 6: COW, 7: CAT, 10: HORSE, 11: MOTORCYCLE, 13: AIRPLANE, 15: TRAIN, 19: DOG, 23: CAR
run ./scripts/split_vid.sh to split the videos into multiple bitrates and resolutions.

STEP3: split transformed videos into image frames


