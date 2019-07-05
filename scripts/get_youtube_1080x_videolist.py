#TODO: list all video that has 1080x1920 resolutions
#INPUT: csv files contain videos in train dataset. Source: https://research.google.com/youtube-bb/
#OUTPUT: list of video id which has resolution 1080x1920
import pandas as pd
import numpy as np
import requests


#get list of all youtube id
df = pd.DataFrame.from_csv('/home/u9167/content_aware/data/YOUTUBE_data/yt_bb_detection_train.csv')
#now extract youtube id_list
col1 = df.iloc[:,0]
id_list = list(set(col1.keys()))
np.random.shuffle(id_list)

#crawl the website, search for 1920x1080 videos only
#    then, output the video ID into file
with open('./data/YOUTUBE_data/youtube_1080_vidlist.txt', 'a') as f:
    url_template="http://www.youtube.com/watch?v={}"
    for vid in id_list:
        url = url_template.format(vid)
        r = requests.get(url=url)
        pos = r.content.find('1920x1080')
        if pos >=0: 
            print vid
            print r.content[pos:pos+200]
            print '-----'
            f.writelines('{}\n'.format(vid))
            f.flush()